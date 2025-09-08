"""Configuration for the EnformionGO API wrapper."""

import os

from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    GALAXY_AP_NAME: str
    GALAXY_AP_PASSWORD: SecretStr  # Use SecretStr for sensitive values

    PERSON_SEARCH_API_URL: str = "https://devapi.enformion.com/PersonSearch"
    REVERSE_PHONE_API_URL: str = "https://devapi.enformion.com/ReversePhoneSearch"
    CONTACT_ENRICHMENT_API_URL: str = "https://devapi.enformion.com/Contact/Enrich"
    CALLER_ID_API_URL: str = "https://devapi.enformion.com/Phone/Enrich"
    EMAIL_ID_API_URL: str = "https://devapi.enformion.com/Email/Enrich"
    CONTACT_ID_API_URL: str = "https://devapi.enformion.com/Contact/Id"
    ADDRESS_ID_API_URL: str = "https://devapi.enformion.com/Address/Id"
    ADDRESS_AUTOCOMPLETE_API_URL: str = "https://devapi.enformion.com/Address/AutoComplete"
    ID_VERIFICATION_API_URL: str = "https://devapi.enformion.com/Identity/Verify_ID"
    CENSUS_SEARCH_API_URL: str = "https://devapi.enformion.com/CensusSearch"
    DIVORCE_SEARCH_API_URL: str = "https://devapi.enformion.com/DivorceSearch"
    LINKEDIN_ID_API_URL: str = "https://devapi.enformion.com/Linkedin/Id"
    PROPERTY_SEARCH_V2_API_URL: str = "https://devapi.enformion.com/PropertyV2Search"
    BUSINESS_SEARCH_V2_API_URL: str = "https://devapi.enformion.com/BusinessSearchV2"
    DOMAIN_SEARCH_API_URL: str = "https://devapi.enformion.com/DomainSearch"
    WORKPLACE_SEARCH_API_URL: str = "https://devapi.enformion.com/WorkplaceSearch"
    BUSINESS_ID_API_URL: str = "https://devapi.enformion.com/BusinessID"

    class Config:
        """Pydantic settings configuration."""

        env_file = ".env"


settings = Settings()