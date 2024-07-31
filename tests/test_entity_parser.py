from typing import List
import unittest

from entity_parser.entity import Entity, EntityField, RefEntityField
from entity_parser.entity_parser import JsonSchemaParser

ZERO: int = 0
ONE: int = 1
TWO: int = 2
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

PRODUCT_BRAND_ENTITY = Entity(
    name='Brand',
    non_ref_fields=[
        EntityField(
            name='name',
            field_type='string',
            max_length=50,
            is_required=True,
            is_primary_key=False,
            type_ref=None
        ),
        EntityField(
            name='description',
            field_type='string',
            max_length='max',
            is_required=False,
            is_primary_key=False,
            type_ref=None
        )
    ],
    ref_fields=[],
    pk_fields=[
        EntityField(
            name='brand_id',
            field_type='string',
            max_length=30,
            is_required=True,
            is_primary_key=False,
            type_ref=None
        )
    ]
)

PRODUCT_CATEGORY_NON_REF_FIELDS = [
    EntityField(
        name='name',
        field_type='string',
        max_length=50,
        is_required=True,
        is_primary_key=False,
        type_ref=None
    ),
    EntityField(
        name='description',
        field_type='string',
        max_length='max',
        is_required=False,
        is_primary_key=False,
        type_ref=None
    )
]

PRODUCT_CATEGORY_PK_FIELDS = [
    EntityField(
        name='id',
        field_type='string',
        max_length=30,
        is_required=True,
        is_primary_key=False,
        type_ref=None
    )
]

PRODUCT_NON_REF_FIELDS = [
    EntityField(
        name='name',
        field_type='string',
        max_length=50,
        is_required=True,
        is_primary_key=False,
        type_ref=None
    ),
    EntityField(
        name='description',
        field_type='string',
        max_length='max',
        is_required=False,
        is_primary_key=False,
        type_ref=None
    ),
    EntityField(
        name='price',
        field_type='number',
        max_length=None,
        is_required=False,
        is_primary_key=False,
        type_ref=None,
        format="decimal"
    ),
    EntityField(
        name='quantity',
        field_type='integer',
        max_length=None,
        is_required=False,
        is_primary_key=False,
        type_ref=None
    ),
]

PRODUCT_PK_FIELDS = [
    EntityField(
        name='productId',
        field_type='string',
        max_length=30,
        is_required=True,
        is_primary_key=False,
        type_ref=None,
        format="uuid"
    )
]

PRODUCT_BRAND_REF_ENTITY = RefEntityField(
    name='brand',
    ref_entity=PRODUCT_BRAND_ENTITY,
    is_required=False
)


class TestJsonSchemaParser(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.parser = JsonSchemaParser()

    def test_brand_json_schema(self):
        actual_entities: List[Entity] = self.parser.parse(
            file_content=BRAND_JSON_SCHEMA
        )
        self.assertEqual(ONE, len(actual_entities))
        self.assertEqual("Brand", actual_entities[0].name)
        self.assertEqual(
            ENTITY_NON_REF_FIELDS, actual_entities[0].non_ref_fields
        )
        self.assertEqual(
            ENTITY_ID_PK_FIELD, actual_entities[0].pk_fields
        )
        self.assertFalse(
            actual_entities[0].ref_fields
        )

    def test_category_json_schema(self):
        actual_entities: List[Entity] = self.parser.parse(
            file_content=CATEGORY_JSON_SCHEMA
        )
        self.assertEqual(ONE, len(actual_entities))
        self.assertEqual("Category", actual_entities[0].name)
        self.assertEqual(
            ENTITY_NON_REF_FIELDS, actual_entities[0].non_ref_fields
        )
        self.assertEqual(
            ENTITY_ID_PK_FIELD, actual_entities[0].pk_fields
        )
        self.assertTrue(
            actual_entities[0].ref_fields
        )
        self.assertEqual(
            ONE, len(actual_entities[0].ref_fields)
        )

        # Verify parent category
        parent_category = actual_entities[0].ref_fields[0]
        self.assertEqual("parent_category", parent_category.name)
        self.assertEqual("Category", parent_category.ref_entity.name)
        self.assertEqual(
            ENTITY_NON_REF_FIELDS,
            parent_category.ref_entity.non_ref_fields
        )
        self.assertEqual(
            ENTITY_ID_PK_FIELD, parent_category.ref_entity.pk_fields
        )

    def test_product_json_schema(self):
        actual_entities: List[Entity] = self.parser.parse(
            file_content=PRODUCT_JSON_SCHEMA
        )
        self.assertEqual(len(actual_entities), THREE)
        actual_entities.sort(key=lambda x: x.name)

        # verify brand
        self.assertEqual(PRODUCT_BRAND_ENTITY, actual_entities[ZERO])

        # Verify category
        category = actual_entities[ONE]
        self.assertEqual("Category", category.name)
        self.assertEqual(
            PRODUCT_CATEGORY_NON_REF_FIELDS, category.non_ref_fields
        )
        self.assertEqual(
            PRODUCT_CATEGORY_PK_FIELDS, category.pk_fields
        )
        self.assertTrue(category.ref_fields)
        self.assertEqual(ONE, len(category.ref_fields))

        # Verify parent category
        parent_category = category.ref_fields[0]
        self.assertEqual("parent_category", parent_category.name)
        self.assertFalse(parent_category.is_required)
        self.assertEqual("Category", parent_category.ref_entity.name)
        self.assertEqual(
            PRODUCT_CATEGORY_NON_REF_FIELDS,
            parent_category.ref_entity.non_ref_fields
        )
        self.assertEqual(
            PRODUCT_CATEGORY_PK_FIELDS, parent_category.ref_entity.pk_fields
        )

        # Verify product
        product = actual_entities[TWO]
        self.assertEqual("Product", product.name)
        self.assertEqual(PRODUCT_NON_REF_FIELDS, product.non_ref_fields)
        self.assertEqual(PRODUCT_PK_FIELDS, product.pk_fields)
        self.assertTrue(product.ref_fields)
        self.assertEqual(TWO, len(product.ref_fields))

        # Verify product ref fields
        product_ref_fields = product.ref_fields
        product_ref_fields.sort(key=lambda x: x.name)

        # Verify product brand reference
        self.assertEqual(PRODUCT_BRAND_REF_ENTITY, product_ref_fields[ZERO])

        # Verify product category reference
        category_ref = product_ref_fields[ONE]
        self.assertEqual("category", category_ref.name)
        self.assertFalse(category_ref.is_required)

        # Verify product category reference entity
        ref_entity = category_ref.ref_entity
        self.assertEqual("Category", ref_entity.name)
        self.assertEqual(
            PRODUCT_CATEGORY_NON_REF_FIELDS, ref_entity.non_ref_fields
        )
        self.assertEqual(
            PRODUCT_CATEGORY_PK_FIELDS, ref_entity.pk_fields
        )


if __name__ == '__main__':
    unittest.main()
