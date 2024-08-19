import unittest

from data_type_mapper.sql_type_mapper import PgsqlTypeMapper
from service_gens.csharp_service_gen.csharp_service_gen import (
    CsharpRestServiceGenerator
)
from sql_generator.sql_generator import (
    PgsqlCommandGenerator, PgsqlTableSqlGenerator
)


OUTPUT_PATH: str = ""

SELF_REF_AND_ENTITY_REF_SCHEMA: str = '''
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "definitions": {
    "Category": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Unique identifier for the category",
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
        "brand_id": {
          "type": "string",
          "description": "Unique identifier for the brand",
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
      "required": ["brand_id", "name"],
      "additionalProperties": false
    },
    "Product": {
      "type": "object",
      "properties": {
        "productId": {
          "type": "string",
          "format": "uuid",
          "description": "Unique identifier for the product",
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


class TestDotnetProcessRunner(unittest.TestCase):
    def test_gen_rest_service(self):
        CsharpRestServiceGenerator.gen_services_from_file_content(
            output_path=OUTPUT_PATH,
            sln_name="Ecommerce",
            service_name="ProductApi",
            file_content=SELF_REF_AND_ENTITY_REF_SCHEMA,
            sql_gen=PgsqlCommandGenerator(entity=None),
            db_type_mapper=PgsqlTypeMapper(),
            db_script_gen=PgsqlTableSqlGenerator()
        )
        self.assertTrue(True)
