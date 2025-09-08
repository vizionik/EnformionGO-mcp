from typing import List, Optional
import logging
from enum import Enum
import httpx
from fastapi import FastAPI, Header, HTTPException, Depends
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi_mcp import FastApiMCP

from config import Settings, settings
from error_handling import http_exception_handler, enformiongo_exception_handler
from exceptions import APIConnectionError, InvalidRequestError
from logging_config import setup_logging
from models import (
    PropertySearchV2Request,
    DomainSearchRequest,
    WorkplaceSearchRequest,
    BusinessIDRequest,
    PersonSearchRequest,
    ContactEnrichmentRequest,
    ReversePhoneSearchRequest,
    CallerIdRequest,
    EmailIdRequest,
    ContactIdRequest,
    AddressIdRequest,
    AddressAutoCompleteRequest,
    IdVerificationRequest,
    CensusSearchRequest,
    DivorceSearchRequest,
    LinkedInIdRequest,
    BusinessSearchRequest,
)

# --- Logging Setup ---
setup_logging()
logger = logging.getLogger(__name__)


# --- Configuration ---
def get_settings():
    return settings


# --- Enums ---
class PersonSearchType(str, Enum):
    person = "Person"
    teaser = "Teaser"


# --- Validation Dependencies ---
def validate_contact_enrichment_request(request: ContactEnrichmentRequest):
    """Dependency to validate that at least two search criteria are provided."""
    criteria_count = 0
    # A name counts as one criterion
    if request.first_name or request.middle_name or request.last_name:
        criteria_count += 1
    if request.phone:
        criteria_count += 1
    if request.address:
        criteria_count += 1
    if request.email:
        criteria_count += 1
    
    if criteria_count < 2:
        raise HTTPException(
            status_code=400,
            detail="Contact Enrichment requires at least two search criteria from: Name, Phone, Address, or Email."
        )
    return request

def validate_id_verification_request(request: IdVerificationRequest):
    """Dependency to validate that at least two ID verification criteria are provided."""
    criteria_count = 0
    if request.first_name or request.middle_name or request.last_name:
        criteria_count += 1
    if request.phones:
        criteria_count += 1
    if request.address_line_1 or request.address_line_2:
        criteria_count += 1
    if request.emails:
        criteria_count += 1
    if request.ssn:
        criteria_count +=1
    
    if criteria_count < 2:
        raise HTTPException(
            status_code=400,
            detail="ID Verification requires at least two criteria from: SSN, Name, Phone, Address, or Email."
        )
    return request


# --- API Helper Function ---
async def call_enformion_api(
    api_url: str, search_type: str, request_body: dict, settings: Settings = Depends(get_settings)
):
    """Generic helper to call the EnformionGO API."""
    if not settings.GALAXY_AP_NAME or not settings.GALAXY_AP_PASSWORD:
        raise APIConnectionError(
            "API credentials (GALAXY_AP_NAME, GALAXY_AP_PASSWORD) are not configured."
        )

    headers = {
        "galaxy-ap-name": settings.GALAXY_AP_NAME,
        "galaxy-ap-password": settings.GALAXY_AP_PASSWORD.get_secret_value(),
        "galaxy-search-type": search_type,
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            response = await client.post(api_url, json=request_body, headers=headers)
            response.raise_for_status()
        except httpx.TimeoutException as exc:
            raise APIConnectionError(f"Request to EnformionGO API timed out: {exc}")
        except httpx.RequestError as exc:
            raise APIConnectionError(f"Error communicating with EnformionGO API: {exc}")
        except httpx.HTTPStatusError as exc:
            logger.error(
                f"Invalid request to EnformionGO API. Status: {exc.response.status_code}, Response: {exc.response.text}"
            )
            raise InvalidRequestError("The request to the upstream service failed.")
    return response.json()


# --- FastAPI Application ---
app = FastAPI(
    title="EnformionGO API Wrapper",
    description="A wrapper for the EnformionGO API Endpoints. With a Twist, MCP-enabled using FastMCP.",
    version="1.7.0",
)

mcp = FastApiMCP(
    app,
    name="EnformionGO MCPServer",
    description="EnformionGO API Wrapped using FastAPI & converted into an http MCPServer using FastApiMCP **NOTE** This is a Bring your own API KEY tool which can be obtainedfrom http://api.enformiongo.com",
)

mcp.mount_http()

# --- Exception Handlers ---
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(APIConnectionError, enformiongo_exception_handler)
app.add_exception_handler(InvalidRequestError, enformiongo_exception_handler)


# --- Endpoints ---

# --- Dev APIs (Single Result) Endpoints ---
@app.post("/contact-enrichment", tags=["Dev APIs (Single Result)"])
async def contact_enrichment(
    search_request: ContactEnrichmentRequest = Depends(validate_contact_enrichment_request),
    settings: Settings = Depends(get_settings),
):
    """Performs a contact enrichment search. Requires at least two criteria."""
    request_body = search_request.model_dump(by_alias=True, exclude_none=True)
    return await call_enformion_api(
        settings.CONTACT_ENRICHMENT_API_URL, "DevAPIContactEnrich", request_body, settings
    )

@app.post("/caller-id", tags=["Dev APIs (Single Result)"])
async def caller_id(search_request: CallerIdRequest, settings: Settings = Depends(get_settings)):
    """Retrieves information associated with a provided phone number."""
    request_body = search_request.model_dump(by_alias=True, exclude_none=True)
    return await call_enformion_api(settings.CALLER_ID_API_URL, "DevAPICallerID", request_body, settings)

@app.post("/email-id", tags=["Dev APIs (Single Result)"])
async def email_id(search_request: EmailIdRequest, settings: Settings = Depends(get_settings)):
    """Retrieves information associated with a provided email address."""
    request_body = search_request.model_dump(by_alias=True, exclude_none=True)
    return await call_enformion_api(settings.EMAIL_ID_API_URL, "DevAPIEmailID", request_body, settings)

@app.post("/contact-id", tags=["Dev APIs (Single Result)"])
async def contact_id(search_request: ContactIdRequest, settings: Settings = Depends(get_settings)):
    """Searches for contact information using a unique person ID."""
    request_body = search_request.model_dump(by_alias=True, exclude_none=True)
    return await call_enformion_api(settings.CONTACT_ID_API_URL, "DevAPIContactID", request_body, settings)

@app.post("/address-id", tags=["Dev APIs (Single Result)"])
async def address_id(search_request: AddressIdRequest, settings: Settings = Depends(get_settings)):
    """Finds contact info for current owners or residents of a property."""
    request_body = search_request.model_dump(by_alias=True, exclude_none=True)
    return await call_enformion_api(settings.ADDRESS_ID_API_URL, "DevAPIAddressID", request_body, settings)

@app.post("/address-autocomplete", tags=["Dev APIs (Single Result)"])
async def address_autocomplete(
    search_request: AddressAutoCompleteRequest, settings: Settings = Depends(get_settings)
):
    """Provides address autocomplete functionality."""
    request_body = search_request.model_dump(by_alias=True, exclude_none=True)
    return await call_enformion_api(
        settings.ADDRESS_AUTOCOMPLETE_API_URL, "DevAPIAddressAutoComplete", request_body, settings
    )

# --- People Data Endpoints ---
@app.post("/person-search", tags=["People Data"])
async def person_search(
    search_request: PersonSearchRequest,
    settings: Settings = Depends(get_settings),
    galaxy_search_type: PersonSearchType = Header(PersonSearchType.person, description="Search type."),
):
    """Performs a person search by proxying the request to the EnformionGO API."""
    request_body = search_request.model_dump(by_alias=True, exclude_none=True)
    return await call_enformion_api(
        settings.PERSON_SEARCH_API_URL, galaxy_search_type.value, request_body, settings
    )

@app.post("/reverse-phone-search", tags=["People Data"])
async def reverse_phone_search(
    search_request: ReversePhoneSearchRequest, settings: Settings = Depends(get_settings)
):
    """Performs a reverse phone search by proxying the request to the EnformionGO API."""
    request_body = search_request.model_dump(by_alias=True, exclude_none=True)
    return await call_enformion_api(settings.REVERSE_PHONE_API_URL, "ReversePhone", request_body, settings)

@app.post("/id-verification", tags=["People Data"])
async def id_verification(
    search_request: IdVerificationRequest = Depends(validate_id_verification_request),
    settings: Settings = Depends(get_settings),
):
    """Provides an identity score and verification flag. Requires at least two criteria."""
    request_body = search_request.model_dump(by_alias=True, exclude_none=True)
    return await call_enformion_api(
        settings.ID_VERIFICATION_API_URL, "DevAPIIDVerification", request_body, settings
    )

@app.post("/census-search", tags=["People Data"])
async def census_search(search_request: CensusSearchRequest, settings: Settings = Depends(get_settings)):
    """Searches historical population data."""
    request_body = search_request.model_dump(by_alias=True, exclude_none=True)
    return await call_enformion_api(settings.CENSUS_SEARCH_API_URL, "Census", request_body, settings)

@app.post("/divorce-search", tags=["People Data"])
async def divorce_search(search_request: DivorceSearchRequest, settings: Settings = Depends(get_settings)):
    """Searches for divorce records."""
    request_body = search_request.model_dump(by_alias=True, exclude_none=True)
    return await call_enformion_api(settings.DIVORCE_SEARCH_API_URL, "Divorce", request_body, settings)

@app.post("/linkedin-id", tags=["People Data"])
async def linkedin_id(search_request: LinkedInIdRequest, settings: Settings = Depends(get_settings)):
    """Searches by a LinkedIn profile URL."""
    request_body = search_request.model_dump(by_alias=True, exclude_none=True)
    return await call_enformion_api(settings.LINKEDIN_ID_API_URL, "LinkedinID", request_body, settings)


# --- Property Data Endpoints ---
@app.post("/property-search-v2", tags=["Property Data"])
async def property_search_v2(
    search_request: PropertySearchV2Request,
    settings: Settings = Depends(get_settings),
    galaxy_search_type: str = Header(..., description="The galaxy-search-type for Property Search V2."),
):
    """
    Searches for property data.
    """
    request_body = search_request.model_dump(by_alias=True, exclude_none=True)
    return await call_enformion_api(
        settings.PROPERTY_SEARCH_V2_API_URL, galaxy_search_type, request_body, settings
    )

# --- Business Data Endpoints ---
@app.post("/business-search", tags=["Business Data"])
async def business_search(
    search_request: BusinessSearchRequest, settings: Settings = Depends(get_settings)
):
    """
    Searches for business data using various criteria.
    """
    request_body = search_request.model_dump(by_alias=True, exclude_none=True)
    return await call_enformion_api(settings.BUSINESS_SEARCH_V2_API_URL, "Business", request_body, settings)

@app.post("/business-search-v2", tags=["Business Data"])
async def business_search_v2(
    search_request: BusinessSearchRequest,
    settings: Settings = Depends(get_settings),
    galaxy_search_type: str = Header(..., description="The galaxy-search-type for Business Search V2."),
):
    """
    Searches for business data using various criteria.
    """
    request_body = search_request.model_dump(by_alias=True, exclude_none=True)
    return await call_enformion_api(
        settings.BUSINESS_SEARCH_V2_API_URL, galaxy_search_type, request_body, settings
    )

@app.post("/domain-search", tags=["Business Data"])
async def domain_search(
    search_request: DomainSearchRequest,
    settings: Settings = Depends(get_settings),
    galaxy_search_type: str = Header(..., description="The galaxy-search-type for Domain Search."),
):
    """
    Searches for domain data.
    """
    request_body = search_request.model_dump(by_alias=True, exclude_none=True)
    return await call_enformion_api(settings.DOMAIN_SEARCH_API_URL, galaxy_search_type, request_body, settings)

@app.post("/workplace-search", tags=["Business Data"])
async def workplace_search(
    search_request: WorkplaceSearchRequest,
    settings: Settings = Depends(get_settings),
    galaxy_search_type: str = Header(..., description="The galaxy-search-type for Workplace Search."),
):
    """
    Searches for workplace data.
    """
    request_body = search_request.model_dump(by_alias=True, exclude_none=True)
    return await call_enformion_api(
        settings.WORKPLACE_SEARCH_API_URL, galaxy_search_type, request_body, settings
    )

@app.post("/business-id", tags=["Business Data"])
async def business_id(
    search_request: BusinessIDRequest,
    settings: Settings = Depends(get_settings),
    galaxy_search_type: str = Header(..., description="The galaxy-search-type for Business ID Search."),
):
    """
    Searches by business ID.
    """
    request_body = search_request.model_dump(by_alias=True, exclude_none=True)
    return await call_enformion_api(settings.BUSINESS_ID_API_URL, galaxy_search_type, request_body, settings)


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


mcp.setup_server()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
