from typing import List
import unittest

from entity_parser.entity import Entity, EntityField
from entity_parser.entity_parser import JsonSchemaParser

ONE: int = 1
THREE: int = 3

BRAND_JSON_SCHEMA: str = '''
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "definitions": {
    "Brand": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Unique identifier for the brand",
          "primaryKey": true,
          "maxLength": 30
        },
        "name": {
          "type": "string",
          "description": "Name of the brand",
          "maxLength": 50
        },
        "description": {
          "type": "string",
          "description": "Description of the brand",
          "maxLength": "max"
        }
      },
      "required": ["id", "name"],
      "additionalProperties": false
    }
  }
}
'''

CATEGORY_JSON_SCHEMA: str = '''
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "definitions": {
    "Category": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Unique identifier for the category",
          "primaryKey": true,
          "maxLength": 30
        },
        "name": {
          "type": "string",
          "description": "Name of the category",
          "maxLength": 50
        },
        "description": {
          "type": "string",
          "description": "Description of the category",
          "maxLength": "max"
        },
        "parent_category": {
          "$ref": "#/definitions/Category",
          "description": "Parent category associated with the category"
        }
      },
      "required": ["id", "name"],
      "additionalProperties": false
    }
  }
}
'''

PRODUCT_JSON_SCHEMA: str = '''
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "definitions": {
    "Category": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Unique identifier for the category",
          "primaryKey": true,
          "maxLength": 30
        },
        "name": {
          "type": "string",
          "description": "Name of the category",
          "maxLength": 50
        },
        "description": {
          "type": "string",
          "description": "Description of the category",
          "maxLength": "max"
        },
        "parent_category": {
          "$ref": "#/definitions/Category",
          "description": "Parent category associated with the category"
        }
      },
      "required": ["id", "name"],
      "additionalProperties": false
    },
    "Brand": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Unique identifier for the brand",
          "primaryKey": true,
          "maxLength": 30
        },
        "name": {
          "type": "string",
          "description": "Name of the brand",
          "maxLength": 50
        },
        "description": {
          "type": "string",
          "description": "Description of the brand",
          "maxLength": "max"
        }
      },
      "required": ["id", "name"],
      "additionalProperties": false
    },
    "Product": {
      "type": "object",
      "properties": {
        "productId": {
          "type": "string",
          "description": "Unique identifier for the product",
          "primaryKey": true,
          "maxLength": 30
        },
        "name": {
          "type": "string",
          "description": "Name of the product",
          "maxLength": 50
        },
        "description": {
          "type": "string",
          "description": "Description of the product",
          "maxLength": "max"
        },
        "price": {
          "type": "number",
          "format": "decimal",
          "description": "Price of the product"
        },
        "quantity": {
          "type": "integer",
          "description": "The quantity of the product currently in stock"
        },
        "brand": {
          "$ref": "#/definitions/Brand",
          "description": "The product brand"
        },
        "category": {
          "$ref": "#/definitions/Category",
          "description": "The product category"
        }
      },
      "required": ["productId", "name"],
      "additionalProperties": false
    }
  }
}
'''

ENTITY_NON_REF_FIELDS = [
    EntityField(
        name="name",
        field_type="string",
        max_length=50,
        is_required=True,
        is_primary_key=False
    ),
    EntityField(
        name="description",
        field_type="string",
        max_length="max",
        is_required=False,
        is_primary_key=False
    )
]

ENTITY_ID_PK_FIELD = [
    EntityField(
        name="id",
        field_type="string",
        max_length=30,
        is_required=True,
        is_primary_key=True
    )
]


class TestJsonSchemaParser(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.parser = JsonSchemaParser()

    def test_brand_json_schema(self):
        actual_entities: List[Entity] = self.parser.parse(
            file_content=BRAND_JSON_SCHEMA
        )
        self.assertEqual(len(actual_entities), ONE)
        self.assertEqual(actual_entities[0].name, "Brand")
        self.assertEqual(
            actual_entities[0].non_ref_fields, ENTITY_NON_REF_FIELDS
        )
        self.assertEqual(
            actual_entities[0].pk_fields, ENTITY_ID_PK_FIELD
        )
        self.assertFalse(
            actual_entities[0].ref_fields
        )

    def test_category_json_schema(self):
        actual_entities: List[Entity] = self.parser.parse(
            file_content=CATEGORY_JSON_SCHEMA
        )
        self.assertEqual(len(actual_entities), ONE)
        self.assertEqual(actual_entities[0].name, "Category")
        self.assertEqual(
            actual_entities[0].non_ref_fields, ENTITY_NON_REF_FIELDS
        )
        self.assertEqual(
            actual_entities[0].pk_fields, ENTITY_ID_PK_FIELD
        )
        self.assertTrue(
            actual_entities[0].ref_fields
        )

    def test_product_json_schema(self):
        actual_entities: List[Entity] = self.parser.parse(
            file_content=PRODUCT_JSON_SCHEMA
        )
        self.assertEqual(len(actual_entities), THREE)


if __name__ == '__main__':
    unittest.main()
