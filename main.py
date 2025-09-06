import os
from typing import List, Optional, Dict, Any

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi_mcp import FastApiMCP
from pydantic import BaseModel, Field

# Load environment variables from a .env file
load_dotenv()

# --- Configuration ---
# API credentials are loaded from a .env file.
# API URLs for the different EnformionGO endpoints.
PERSON_SEARCH_API_URL = "https://devapi.enformion.com/PersonSearch"
REVERSE_PHONE_API_URL = "https://devapi.enformion.com/ReversePhoneSearch"
CONTACT_ENRICHMENT_API_URL = "https://devapi.enformion.com/Contact/Enrich"
CALLER_ID_API_URL = "https://devapi.enformion.com/Phone/Enrich"
EMAIL_ID_API_URL = "https://devapi.enformion.com/Email/Enrich"
CONTACT_ID_API_URL = "https://devapi.enformion.com/Contact/Id"
ADDRESS_ID_API_URL = "https://devapi.enformion.com/Address/Id"
ADDRESS_AUTOCOMPLETE_API_URL = "https://devapi.enformion.com/Address/AutoComplete"
ID_VERIFICATION_API_URL = "https://devapi.enformion.com/Identity/Verify_ID"
CENSUS_SEARCH_API_URL = "https://devapi.enformion.com/CensusSearch"
DIVORCE_SEARCH_API_URL = "https://devapi.enformion.com/DivorceSearch"
LINKEDIN_ID_API_URL = "https://devapi.enformion.com/Linkedin/Id"
PROPERTY_SEARCH_V2_API_URL = "https://devapi.enformion.com/PropertyV2Search"
BUSINESS_SEARCH_V2_API_URL = "https://devapi.enformion.com/BusinessSearchV2"
DOMAIN_SEARCH_API_URL = "https://devapi.enformion.com/DomainSearch"
WORKPLACE_SEARCH_API_URL = "https://devapi.enformion.com/WorkplaceSearch"
BUSINESS_ID_API_URL = "https://devapi.enformion.com/BusinessID"
GALAXY_AP_NAME = os.environ.get("GALAXY_AP_NAME")
GALAXY_AP_PASSWORD = os.environ.get("GALAXY_AP_PASSWORD")


# --- Pydantic Models for Request Bodies ---

class Address(BaseModel):
    """Represents an address for the person search."""
    address_line_1: Optional[str] = Field(None, alias="addressLine1")
    address_line_2: Optional[str] = Field(None, alias="addressLine2")
    county: Optional[str] = Field(None, alias="County")

class Name(BaseModel):
    """Represents a name, used for AKAs and relatives."""
    first_name: Optional[str] = Field(None, alias="FirstName")
    middle_name: Optional[str] = Field(None, alias="MiddleName")
    last_name: Optional[str] = Field(None, alias="LastName")

class PersonSearchRequest(BaseModel):
    """Defines the request body for the Person Search API."""
    first_name: Optional[str] = Field(None, alias="FirstName")
    middle_name: Optional[str] = Field(None, alias="MiddleName")
    last_name: Optional[str] = Field(None, alias="LastName")
    akas: Optional[List[Name]] = Field(None, alias="Akas")
    dob: Optional[str] = Field(None, alias="Dob")
    age: Optional[int] = Field(None, alias="Age")
    age_range_min_age: Optional[int] = Field(None, alias="AgeRangeMinAge")
    age_range_max_age: Optional[int] = Field(None, alias="AgeRangeMaxAge")
    age_range: Optional[str] = Field(None, alias="AgeRange")
    ssn: Optional[str] = Field(None, alias="Ssn")
    addresses: Optional[List[Address]] = Field(None, alias="Addresses")
    email: Optional[str] = Field(None, alias="Email")
    client_ip: Optional[str] = Field(None, alias="ClientIp")
    phone: Optional[str] = Field(None, alias="Phone")
    relatives: Optional[List[Name]] = Field(None, alias="Relatives")
    tahoe_ids: Optional[List[str]] = Field(None, alias="TahoeIds")
    first_name_char_offset: Optional[int] = Field(None, alias="FirstNameCharOffset")
    last_name_char_offset: Optional[int] = Field(None, alias="LastNameCharOffset")
    dob_format: Optional[str] = Field(None, alias="DobFormat")
    max_address_years: Optional[int] = Field(None, alias="MaxAddressYears")
    max_phone_years: Optional[int] = Field(None, alias="MaxPhoneYears")

    class Config:
        """Pydantic config to allow population by alias."""
        populate_by_name = True
        
class ContactEnrichmentAddress(BaseModel):
    """Represents an address specifically for Contact Enrichment."""
    address_line_1: Optional[str] = Field(None, alias="addressLine1")
    address_line_2: Optional[str] = Field(None, alias="addressLine2")

class ContactEnrichmentRequest(BaseModel):
    """Defines the request body for the Contact Enrichment API."""
    first_name: Optional[str] = Field(None, alias="FirstName")
    middle_name: Optional[str] = Field(None, alias="MiddleName")
    last_name: Optional[str] = Field(None, alias="LastName")
    dob: Optional[str] = Field(None, alias="Dob")
    age: Optional[int] = Field(None, alias="Age")
    address: Optional[ContactEnrichmentAddress] = Field(None, alias="Address")
    phone: Optional[str] = Field(None, alias="Phone")
    email: Optional[str] = Field(None, alias="Email")

    class Config:
        """Pydantic config to allow population by alias."""
        populate_by_name = True

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

class ReversePhoneSearchRequest(BaseModel):
    """Defines the request body for the Reverse Phone Search API."""
    phone: str = Field(..., alias="Phone", description="The phone number to search for (e.g., '123-456-7890').")
    page: Optional[int] = Field(1, alias="Page", description="The page of data to return.")
    results_per_page: Optional[int] = Field(10, alias="ResultsPerPage", description="The number of results to return per page.")

    class Config:
        """Pydantic config to allow population by alias."""
        populate_by_name = True

class CallerIdRequest(BaseModel):
    """Defines the request body for the Caller ID API."""
    phone: str = Field(..., alias="Phone")

    class Config:
        populate_by_name = True

class EmailIdRequest(BaseModel):
    """Defines the request body for the Email ID API."""
    email: str = Field(..., alias="Email")

    class Config:
        populate_by_name = True

class ContactIdRequest(BaseModel):
    """Defines the request body for the Contact ID API."""
    person_id: str = Field(..., alias="PersonId")

    class Config:
        populate_by_name = True

class AddressIdRequest(BaseModel):
    """Defines the request body for the Address ID API."""
    address_line_1: str = Field(..., alias="addressLine1")
    address_line_2: str = Field(..., alias="addressLine2")
    exact_match: Optional[str] = Field(None, alias="ExactMatch", description="Can be 'CurrentOwner' or 'CurrentResident'.")

    class Config:
        populate_by_name = True

class AddressAutoCompleteRequest(BaseModel):
    """Defines the request body for the Address AutoComplete API."""
    input_str: str = Field(..., alias="Input")

    class Config:
        populate_by_name = True

class IdVerificationRequest(BaseModel):
    """Defines the request body for the ID Verification API."""
    first_name: Optional[str] = Field(None, alias="FirstName")
    middle_name: Optional[str] = Field(None, alias="MiddleName")
    last_name: Optional[str] = Field(None, alias="LastName")
    dob: Optional[str] = Field(None, alias="Dob")
    age: Optional[int] = Field(None, alias="Age")
    address_line_1: Optional[str] = Field(None, alias="AddressLine1")
    address_line_2: Optional[str] = Field(None, alias="AddressLine2")
    phones: Optional[List[str]] = Field(None, alias="Phones")
    emails: Optional[List[str]] = Field(None, alias="Emails")
    ssn: Optional[str] = Field(None, alias="Ssn")

    class Config:
        populate_by_name = True

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

class CensusAddress(BaseModel):
    city: Optional[str] = Field(None, alias="City")
    county: Optional[str] = Field(None, alias="County")
    state: Optional[str] = Field(None, alias="State")
    zip_code: Optional[str] = Field(None, alias="ZipCode")

class CensusSearchRequest(BaseModel):
    """Defines the request body for the Census Search API."""
    first_name: Optional[str] = Field(None, alias="FirstName")
    middle_name: Optional[str] = Field(None, alias="MiddleName")
    last_name: Optional[str] = Field(None, alias="LastName")
    dob: Optional[str] = Field(None, alias="DOB")
    age: Optional[str] = Field(None, alias="Age")
    addresses: Optional[CensusAddress] = Field(None, alias="Addresses")
    relatives: Optional[List[Name]] = Field(None, alias="Relatives")
    census_decades: Optional[List[int]] = Field(None, alias="CensusDecades")

    class Config:
        populate_by_name = True

class DivorceSearchRequest(BaseModel):
    """Defines the request body for the Divorce Search API."""
    first_name: Optional[str] = Field(None, alias="FirstName")
    middle_name: Optional[str] = Field(None, alias="MiddleName")
    last_name: Optional[str] = Field(None, alias="LastName")
    name_suffix: Optional[str] = Field(None, alias="NameSuffix")
    maiden_name: Optional[str] = Field(None, alias="MaidenName")
    spouse_first_name: Optional[str] = Field(None, alias="SpouseFirstName")
    spouse_middle_name: Optional[str] = Field(None, alias="SpouseMiddleName")
    spouse_last_name: Optional[str] = Field(None, alias="SpouseLastName")
    spouse_name_suffix: Optional[str] = Field(None, alias="SpouseNameSuffix")
    marriage_date: Optional[str] = Field(None, alias="MarriageDate")
    divorce_date: Optional[str] = Field(None, alias="DivorceDate")
    city: Optional[str] = Field(None, alias="City")
    county: Optional[str] = Field(None, alias="County")
    state: Optional[str] = Field(None, alias="State")
    poseidon_ids: Optional[List[str]] = Field(None, alias="PosiedonIds")
    tahoe_id: Optional[str] = Field(None, alias="TahoeId")
    ssn: Optional[str] = Field(None, alias="SSN")
    
    class Config:
        populate_by_name = True

class LinkedInIdRequest(BaseModel):
    """Defines the request body for the LinkedIn ID API."""
    profile_url: str = Field(..., alias="profileURL")

    class Config:
        populate_by_name = True

class BusinessSearchRequest(BaseModel):
    """Defines the request body for the Business Search API."""
    business_name: Optional[str] = Field(None, alias="businessName")
    first_name: Optional[str] = Field(None, alias="firstName")
    middle_name: Optional[str] = Field(None, alias="middleName")
    last_name: Optional[str] = Field(None, alias="lastName")
    creditor_name: Optional[str] = Field(None, alias="creditorName")
    address_line_1: Optional[str] = Field(None, alias="addressLine1")
    address_line_2: Optional[str] = Field(None, alias="addressLine2")
    county: Optional[str] = Field(None, alias="county")
    poseidon_id: Optional[str] = Field(None, alias="poseidonId")
    tahoe_id: Optional[str] = Field(None, alias="tahoeId")
    tax_id: Optional[str] = Field(None, alias="taxId")
    ssn: Optional[str] = Field(None, alias="ssn")
    business_type: Optional[str] = Field(None, alias="businessType")
    page: Optional[int] = Field(None, alias="Page")
    results_per_page: Optional[int] = Field(None, alias="ResultsPerPage")

    class Config:
        populate_by_name = True


# --- API Helper Function ---
async def call_enformion_api(api_url: str, search_type: str, request_body: dict):
    """Generic helper to call the EnformionGO API."""
    if not GALAXY_AP_NAME or not GALAXY_AP_PASSWORD:
        raise HTTPException(
            status_code=500,
            detail="API credentials (GALAXY_AP_NAME, GALAXY_AP_PASSWORD) are not configured."
        )

    headers = {
        "galaxy-ap-name": GALAXY_AP_NAME,
        "galaxy-ap-password": GALAXY_AP_PASSWORD,
        "galaxy-search-type": search_type,
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(api_url, json=request_body, headers=headers)
            response.raise_for_status()
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=503,
                detail=f"Error communicating with EnformionGO API: {exc}"
            )
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=exc.response.json()
            )
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

# --- Endpoints ---

# --- Dev APIs (Single Result) Endpoints ---
@app.post("/contact-enrichment", tags=["Dev APIs (Single Result)"])
async def contact_enrichment(
    search_request: ContactEnrichmentRequest = Depends(validate_contact_enrichment_request)
):
    """Performs a contact enrichment search. Requires at least two criteria."""
    request_body = search_request.model_dump(by_alias=True, exclude_none=True)
    return await call_enformion_api(CONTACT_ENRICHMENT_API_URL, "DevAPIContactEnrich", request_body)

@app.post("/caller-id", tags=["Dev APIs (Single Result)"])
async def caller_id(search_request: CallerIdRequest):
    """Retrieves information associated with a provided phone number."""
    request_body = search_request.model_dump(by_alias=True, exclude_none=True)
    return await call_enformion_api(CALLER_ID_API_URL, "DevAPICallerID", request_body)

@app.post("/email-id", tags=["Dev APIs (Single Result)"])
async def email_id(search_request: EmailIdRequest):
    """Retrieves information associated with a provided email address."""
    request_body = search_request.model_dump(by_alias=True, exclude_none=True)
    return await call_enformion_api(EMAIL_ID_API_URL, "DevAPIEmailID", request_body)

@app.post("/contact-id", tags=["Dev APIs (Single Result)"])
async def contact_id(search_request: ContactIdRequest):
    """Searches for contact information using a unique person ID."""
    request_body = search_request.model_dump(by_alias=True, exclude_none=True)
    return await call_enformion_api(CONTACT_ID_API_URL, "DevAPIContactID", request_body)

@app.post("/address-id", tags=["Dev APIs (Single Result)"])
async def address_id(search_request: AddressIdRequest):
    """Finds contact info for current owners or residents of a property."""
    request_body = search_request.model_dump(by_alias=True, exclude_none=True)
    return await call_enformion_api(ADDRESS_ID_API_URL, "DevAPIAddressID", request_body)

@app.post("/address-autocomplete", tags=["Dev APIs (Single Result)"])
async def address_autocomplete(search_request: AddressAutoCompleteRequest):
    """Provides address autocomplete functionality."""
    request_body = search_request.model_dump(by_alias=True, exclude_none=True)
    return await call_enformion_api(ADDRESS_AUTOCOMPLETE_API_URL, "DevAPIAddressAutoComplete", request_body)

# --- People Data Endpoints ---
@app.post("/person-search", tags=["People Data"])
async def person_search(
    search_request: PersonSearchRequest,
    galaxy_search_type: str = Header("Person", description="Search type (e.g., 'Person', 'Teaser')."),
):
    """Performs a person search by proxying the request to the EnformionGO API."""
    request_body = search_request.model_dump(by_alias=True, exclude_none=True)
    return await call_enformion_api(PERSON_SEARCH_API_URL, galaxy_search_type, request_body)

@app.post("/reverse-phone-search", tags=["People Data"])
async def reverse_phone_search(search_request: ReversePhoneSearchRequest):
    """Performs a reverse phone search by proxying the request to the EnformionGO API."""
    request_body = search_request.model_dump(by_alias=True, exclude_none=True)
    return await call_enformion_api(REVERSE_PHONE_API_URL, "ReversePhone", request_body)

@app.post("/id-verification", tags=["People Data"])
async def id_verification(
    search_request: IdVerificationRequest = Depends(validate_id_verification_request)
):
    """Provides an identity score and verification flag. Requires at least two criteria."""
    request_body = search_request.model_dump(by_alias=True, exclude_none=True)
    return await call_enformion_api(ID_VERIFICATION_API_URL, "DevAPIIDVerification", request_body)

@app.post("/census-search", tags=["People Data"])
async def census_search(search_request: CensusSearchRequest):
    """Searches historical population data."""
    request_body = search_request.model_dump(by_alias=True, exclude_none=True)
    if (request_body.get("Addresses", {}).get("City") or request_body.get("Addresses", {}).get("County")) and not request_body.get("Addresses", {}).get("State"):
        raise HTTPException(status_code=400, detail="State is required if City or County is provided.")
    return await call_enformion_api(CENSUS_SEARCH_API_URL, "Census", request_body)

@app.post("/divorce-search", tags=["People Data"])
async def divorce_search(search_request: DivorceSearchRequest):
    """Searches for divorce records."""
    request_body = search_request.model_dump(by_alias=True, exclude_none=True)
    if request_body.get("City") and not request_body.get("State"):
        raise HTTPException(status_code=400, detail="State is required when City is provided.")
    return await call_enformion_api(DIVORCE_SEARCH_API_URL, "Divorce", request_body)

@app.post("/linkedin-id", tags=["People Data"])
async def linkedin_id(search_request: LinkedInIdRequest):
    """Searches by a LinkedIn profile URL."""
    request_body = search_request.model_dump(by_alias=True, exclude_none=True)
    return await call_enformion_api(LINKEDIN_ID_API_URL, "LinkedinID", request_body)

# --- Property Data Endpoints ---
@app.post("/property-search-v2", tags=["Property Data"])
async def property_search_v2(
    search_request: Dict[str, Any],
    galaxy_search_type: str = Header(..., description="The galaxy-search-type for Property Search V2 (not provided in docs)."),
):
    """
    Searches for property data. The specific JSON properties and galaxy-search-type
    are not defined in the documentation and must be provided by the user.
    """
    return await call_enformion_api(PROPERTY_SEARCH_V2_API_URL, galaxy_search_type, search_request)

# --- Business Data Endpoints ---
@app.post("/business-search", tags=["Business Data"])
async def business_search(search_request: BusinessSearchRequest):
    """
    Searches for business data using various criteria.
    """
    request_body = search_request.model_dump(by_alias=True, exclude_none=True)
    return await call_enformion_api(BUSINESS_SEARCH_V2_API_URL, "BusinessV2", request_body)

@app.post("/domain-search", tags=["Business Data"])
async def domain_search(
    search_request: Dict[str, Any],
    galaxy_search_type: str = Header(..., description="The galaxy-search-type for Domain Search (not provided in docs)."),
):
    """
    Searches for domain data. The specific JSON properties and galaxy-search-type
    are not defined in the documentation and must be provided by the user.
    """
    return await call_enformion_api(DOMAIN_SEARCH_API_URL, galaxy_search_type, search_request)

@app.post("/workplace-search", tags=["Business Data"])
async def workplace_search(
    search_request: Dict[str, Any],
    galaxy_search_type: str = Header("Workplace", description="The galaxy-search-type for Workplace Search"),
):
    """
    Searches for workplace data. The specific JSON properties and galaxy-search-type
    are not defined in the documentation and must be provided by the user.
    """
    return await call_enformion_api(WORKPLACE_SEARCH_API_URL, galaxy_search_type, search_request)

@app.post("/business-id", tags=["Business Data"])
async def business_id(
    search_request: Dict[str, Any],
    galaxy_search_type: str = Header(..., description="The galaxy-search-type for Business ID Search (not provided in docs)."),
):
    """
    Searches by business ID. The specific JSON properties and galaxy-search-type
    are not defined in the documentation and must be provided by the user.
    """
    return await call_enformion_api(BUSINESS_ID_API_URL, galaxy_search_type, search_request)


mcp.setup_server()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
