from pydantic import BaseModel, Field
from typing import List

# Define the WebsiteInfo model
class WebsiteInfo(BaseModel):
    url: str = Field(..., description="URL of the website")  
    site: str = Field(..., description="The name or title of the website or organization")
    description: str = Field(..., description="A brief description of the website's purpose or content")

# Define a model that contains a list of WebsiteInfo models
class WebsiteList(BaseModel):
    websites: List[WebsiteInfo] = Field(..., description="A list of WebsiteInfo objects")