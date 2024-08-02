import textwrap
from typing import List
import unittest
from unittest.mock import mock_open, patch

from entity_parser.entity import Entity, EntityField, FieldType, RefEntityField
from entity_parser.entity_parser import JsonSchemaParser

ZERO: int = 0
ONE: int = 1
TWO: int = 2
THREE: int = 3
THIRTY: int = 30
FIFTY: int = 50

ADDRESS: str = "address"
BRAND: str = "Brand"
CATEGORY: str = "Category"
CITY: str = "city"
DESCRIPTION: str = "description"
ID: str = "id"
MAX_LEN: str = "max"
NAME: str = "name"
PARENT_CATEGORY: str = "parent_category"
STREET: str = "street"

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

INVALID_REF_JSON_SCHEMA: str = '''
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
          "$ref": "#/definitions/files/Category",
          "description": "Parent category associated with the category"
        }
      },
      "required": ["id", "name"],
      "additionalProperties": false
    }
  }
}
'''

INVALID_PRIMARY_KEY_SCHEMA: str = '''
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
          "primaryKey": true,
          "description": "Parent category associated with the category"
        }
      },
      "required": ["id", "name"],
      "additionalProperties": false
    }
  }
}
'''

MISSING_REF_DEFINITION: str = '''
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "definitions": {
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

MISSING_PRIMARY_KEY_SCHEMA: str = '''
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "definitions": {
    "Brand": {
      "type": "object",
      "properties": {
        "data_id": {
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
      "required": ["data_id", "name"],
      "additionalProperties": false
    }
  }
}
'''

TITLE_SCHEMA_WITH_NESTED_OBJECT: str = '''
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Person",
    "type": "object",
    "properties": {
        "name": {
            "type": "string"
        },
        "age": {
            "type": "integer"
        },
        "address": {
            "type": "object",
            "properties": {
                "street": {
                    "type": "string"
                },
                "city": {
                    "type": "string"
                }
            },
            "required": ["street", "city"]
        }
    },
    "required": ["name", "age"]
}
'''


ENTITY_NON_REF_FIELDS = [
    EntityField(
        name=NAME,
        field_type=FieldType.STRING,
        max_length=FIFTY,
        is_required=True,
        is_primary_key=False
    ),
    EntityField(
        name=DESCRIPTION,
        field_type=FieldType.STRING,
        max_length=MAX_LEN,
        is_required=False,
        is_primary_key=False
    )
]

ENTITY_ID_PK_FIELD = [
    EntityField(
        name=ID,
        field_type=FieldType.STRING,
        max_length=THIRTY,
        is_required=True,
        is_primary_key=True
    )
]

PRODUCT_BRAND_ENTITY = Entity(
    name=BRAND,
    non_ref_fields=[
        EntityField(
            name=NAME,
            field_type=FieldType.STRING,
            max_length=FIFTY,
            is_required=True,
            is_primary_key=False,
            type_ref=None
        ),
        EntityField(
            name=DESCRIPTION,
            field_type=FieldType.STRING,
            max_length=MAX_LEN,
            is_required=False,
            is_primary_key=False,
            type_ref=None
        )
    ],
    ref_fields=[],
    pk_fields=[
        EntityField(
            name="brand_id",
            field_type=FieldType.STRING,
            max_length=THIRTY,
            is_required=True,
            is_primary_key=False,
            type_ref=None
        )
    ]
)

PRODUCT_CATEGORY_NON_REF_FIELDS = [
    EntityField(
        name=NAME,
        field_type=FieldType.STRING,
        max_length=FIFTY,
        is_required=True,
        is_primary_key=False,
        type_ref=None
    ),
    EntityField(
        name=DESCRIPTION,
        field_type=FieldType.STRING,
        max_length=MAX_LEN,
        is_required=False,
        is_primary_key=False,
        type_ref=None
    )
]

PRODUCT_CATEGORY_PK_FIELDS = [
    EntityField(
        name=ID,
        field_type=FieldType.STRING,
        max_length=THIRTY,
        is_required=True,
        is_primary_key=False,
        type_ref=None
    )
]

PRODUCT_NON_REF_FIELDS = [
    EntityField(
        name=NAME,
        field_type=FieldType.STRING,
        max_length=FIFTY,
        is_required=True,
        is_primary_key=False,
        type_ref=None
    ),
    EntityField(
        name=DESCRIPTION,
        field_type=FieldType.STRING,
        max_length=MAX_LEN,
        is_required=False,
        is_primary_key=False,
        type_ref=None
    ),
    EntityField(
        name="price",
        field_type=FieldType.NUMBER,
        max_length=None,
        is_required=False,
        is_primary_key=False,
        type_ref=None,
        format="decimal"
    ),
    EntityField(
        name="quantity",
        field_type=FieldType.INTEGER,
        max_length=None,
        is_required=False,
        is_primary_key=False,
        type_ref=None
    ),
]

PRODUCT_PK_FIELDS = [
    EntityField(
        name="productId",
        field_type=FieldType.STRING,
        max_length=THIRTY,
        is_required=True,
        is_primary_key=False,
        type_ref=None,
        format="uuid"
    )
]

PRODUCT_BRAND_REF_ENTITY = RefEntityField(
    name="brand",
    ref_entity=PRODUCT_BRAND_ENTITY,
    is_required=False
)

TITLE_SCHEMA_WITH_NESTED_OBJECT_ENTITIES: List[Entity] = [
    Entity(
        name="Person",
        non_ref_fields=[
            EntityField(
                name="name",
                field_type=FieldType.STRING,
                max_length=None,
                is_required=True,
                is_primary_key=False,
                type_ref=None,
                format=None,
                is_enum=False,
                enum_values=[]
            ),
            EntityField(
                name="age",
                field_type=FieldType.INTEGER,
                max_length=None,
                is_required=True,
                is_primary_key=False,
                type_ref=None,
                format=None,
                is_enum=False,
                enum_values=[]
            )
        ],
        ref_fields=[
            RefEntityField(
                name=ADDRESS,
                ref_entity=Entity(
                    name=ADDRESS,
                    non_ref_fields=[
                        EntityField(
                            name=STREET,
                            field_type=FieldType.STRING,
                            max_length=None,
                            is_required=True,
                            is_primary_key=False,
                            type_ref=None,
                            format=None,
                            is_enum=False,
                            enum_values=[]
                        ),
                        EntityField(
                            name=CITY,
                            field_type=FieldType.STRING,
                            max_length=None,
                            is_required=True,
                            is_primary_key=False,
                            type_ref=None,
                            format=None,
                            is_enum=False,
                            enum_values=[]
                        )
                    ],
                    ref_fields=[],
                    pk_fields=[]
                ),
                is_required=False
            )
        ],
        pk_fields=[]
    ),
    Entity(
        name=ADDRESS,
        non_ref_fields=[
            EntityField(
                name=STREET,
                field_type=FieldType.STRING,
                max_length=None,
                is_required=True,
                is_primary_key=False,
                type_ref=None,
                format=None,
                is_enum=False,
                enum_values=[]
            ),
            EntityField(
                name=CITY,
                field_type=FieldType.STRING,
                max_length=None,
                is_required=True,
                is_primary_key=False,
                type_ref=None,
                format=None,
                is_enum=False,
                enum_values=[]
            )
        ],
        ref_fields=[],
        pk_fields=[]
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
        self.assertEqual(ONE, len(actual_entities))
        self.assertEqual(BRAND, actual_entities[0].name)
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
        self.assertEqual(CATEGORY, actual_entities[0].name)
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
        self.assertEqual(PARENT_CATEGORY, parent_category.name)
        self.assertEqual(CATEGORY, parent_category.ref_entity.name)
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
        self._verify_product_json_schema_test(actual_entities)

    @patch(
        "builtins.open", new_callable=mock_open, read_data=PRODUCT_JSON_SCHEMA
    )
    def test_parser_file_path(self, mock_file):
        file_path = "tests/file/path"
        actual_entities: List[Entity] = self.parser.parse(
            file_path=file_path
        )
        mock_file.assert_called_once_with(file_path)
        self._verify_product_json_schema_test(actual_entities)

    def _verify_product_json_schema_test(
        self, actual_entities: List[Entity]
    ) -> None:
        self.assertEqual(len(actual_entities), THREE)
        actual_entities.sort(key=lambda x: x.name)

        # verify brand
        self.assertEqual(PRODUCT_BRAND_ENTITY, actual_entities[ZERO])

        # Verify category
        category = actual_entities[ONE]
        self.assertEqual(CATEGORY, category.name)
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
        self.assertEqual(PARENT_CATEGORY, parent_category.name)
        self.assertFalse(parent_category.is_required)
        self.assertEqual(CATEGORY, parent_category.ref_entity.name)
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
        self.assertEqual(CATEGORY, ref_entity.name)
        self.assertEqual(
            PRODUCT_CATEGORY_NON_REF_FIELDS, ref_entity.non_ref_fields
        )
        self.assertEqual(
            PRODUCT_CATEGORY_PK_FIELDS, ref_entity.pk_fields
        )

    def test_parser_invalid_ref(self):
        with self.assertRaises(ValueError) as context:
            self.parser.parse(file_content=INVALID_REF_JSON_SCHEMA)
        self.assertEqual(
            "Json schema contains invalid ref `#/definitions/files/Category`",
            str(context.exception)
        )

    def test_parser_invalid_primary_key(self):
        with self.assertRaises(ValueError) as context:
            self.parser.parse(file_content=INVALID_PRIMARY_KEY_SCHEMA)
        self.assertEqual(
            textwrap.dedent(
                """
                Cannot use a referenced entity as primary key field -
                `Category.parent_category`
                """
            ),
            textwrap.dedent(str(context.exception))
        )

    def test_parser_missing_definition(self):
        with self.assertRaises(ValueError) as context:
            self.parser.parse(file_content=MISSING_REF_DEFINITION)
        self.assertEqual(
            textwrap.dedent(
                """
                `Brand` is referenced in `Product` but
                does not have a definition
                """
            ),
            textwrap.dedent(str(context.exception))
        )

    def test_parser_missing_input(self):
        with self.assertRaises(ValueError) as context:
            self.parser.parse()
        self.assertEqual(
            textwrap.dedent(
                """
                Either `file_content` or `file_path` is require but
                none was provided
                """
            ),
            textwrap.dedent(str(context.exception))
        )

    def test_title_schema_with_nested_object(self):
        actual_entities: List[Entity] = self.parser.parse(
            file_content=TITLE_SCHEMA_WITH_NESTED_OBJECT
        )
        self.assertEqual(
            TITLE_SCHEMA_WITH_NESTED_OBJECT_ENTITIES, actual_entities
        )


if __name__ == "__main__":
    unittest.main()
