from pydantic import BaseModel, Field, PrivateAttr
from typing import List, Optional, Union, Any, Dict
import pyparsing as pp

class Item(BaseModel):
    type: str = Field(..., description="The type of item")
    entity: str = Field(..., description="The entity of the item")
    location: str = Field(..., description="The location of the item")
    description: str = Field(..., description="The description of the item")
    
    entity_label : str = Field(..., description="The entity label of the item")

    def __repr__(self):
        return f"{self.entity} {self.location}"