from typing import List
import unittest
from parameterized import parameterized

from entity_parser.entity import Entity, EntityField, FieldType, RefEntityField
from sql_generator.sql_generator import (
    PgsqlCommandGenerator, PgsqlTableSqlGenerator, PgsqlTypeMapper
)

THIRTY: int = 30
FIFTY: int = 50

ADDRESS: str = "address"
CATEGORY: str = "Category"
CITY: str = "city"
DESCRIPTION: str = "description"
MAX_LEN: str = "max"
NAME: str = "name"
STATE: str = "state"
STREET: str = "street"

ENTITY_WITH_NO_REF = Entity(
    name="Brand",
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

CATEGORY_ENTITY = Entity(
    name=CATEGORY,
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
            name="id",
            field_type=FieldType.INTEGER,
            max_length=THIRTY,
            is_required=True,
            is_primary_key=False,
            type_ref=None
        )
    ]
)

ENTITY_WITH_REF = Entity(
    name="product",
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
        )
    ],
    ref_fields=[
        RefEntityField(
            name="brand",
            ref_entity=ENTITY_WITH_NO_REF,
            is_required=True
        ),
        RefEntityField(
            name="category",
            ref_entity=CATEGORY_ENTITY,
            is_required=True
        )
    ],
    pk_fields=[
        EntityField(
            name="productid",
            field_type=FieldType.STRING,
            max_length=THIRTY,
            is_required=True,
            is_primary_key=False,
            type_ref=None,
            format="uuid"
        )
    ]
)

STATE_ENUM_ENTITY = Entity(
    name=STATE,
    non_ref_fields=[],
    ref_fields=[],
    pk_fields=[],
    is_enum=True,
    enum_values=["CA", "NY", "... etc ..."]
)

ADDRESS_ENTITY = Entity(
    name=ADDRESS,
    non_ref_fields=[
        EntityField(
            name="street_address",
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
    ref_fields=[
        RefEntityField(
            name=STATE,
            ref_entity=STATE_ENUM_ENTITY,
            is_required=True
        )
    ],
    pk_fields=[],
    is_enum=False,
    enum_values=None,
    is_sub_def=True
)

CUSTOMER_ENTITY = Entity(
    name="customer",
    non_ref_fields=[
        EntityField(
            name="first_name",
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
            name="last_name",
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
    ref_fields=[
        RefEntityField(
            name="shipping_address",
            ref_entity=ADDRESS_ENTITY,
            is_required=True
        ),
        RefEntityField(
            name="billing_address",
            ref_entity=ADDRESS_ENTITY,
            is_required=True
        )
    ],
    pk_fields=[],
    is_enum=False,
    enum_values=None
)

COMPOSITE_PRIMARY_KEY_ENTITY = Entity(
    name='product_order',
    non_ref_fields=[
        EntityField(
            name='quantity',
            field_type=FieldType.INTEGER,
            max_length=None,
            is_required=True,
            is_primary_key=False,
            type_ref=None,
            format=None,
            is_enum=False,
            enum_values=[],
            minimum=None,
            maximum=None
        ),
        EntityField(
            name='price',
            field_type=FieldType.NUMBER,
            max_length=None,
            is_required=True,
            is_primary_key=False,
            type_ref=None,
            format='float',
            is_enum=False,
            enum_values=[],
            minimum=None,
            maximum=None
        )
    ],
    ref_fields=[],
    pk_fields=[
        EntityField(
            name='order_id',
            field_type=FieldType.INTEGER,
            max_length=None,
            is_required=True,
            is_primary_key=True,
            type_ref=None,
            format=None,
            is_enum=False,
            enum_values=[],
            minimum=None,
            maximum=None
        ),
        EntityField(
            name='product_id',
            field_type=FieldType.INTEGER,
            max_length=None,
            is_required=True,
            is_primary_key=True,
            type_ref=None,
            format=None,
            is_enum=False,
            enum_values=[],
            minimum=None,
            maximum=None
        )
    ],
    is_enum=False,
    enum_values=None,
    is_sub_def=False
)


class TestPostgreSqlGenerator(unittest.TestCase):
    @parameterized.expand([
        (
            "entity_with_no_ref",
            ENTITY_WITH_NO_REF,
            (
                "SELECT brand_id, name, description FROM Brand "
                "WHERE (@brand_ids = {} OR brand_ids = ANY(@brand_ids)) "
                "ORDER BY brand_id ASC LIMIT @limit OFFSET @offset;"
            )
        ),
        (
            "entity_with_ref",
            ENTITY_WITH_REF,
            (
                "SELECT productid, name, description, price, quantity, "
                "brand_id, category_id FROM product "
                "WHERE (@productids = {} OR productids = ANY(@productids)) "
                "AND (@brand_ids = {} OR brand_ids = ANY(@brand_ids)) "
                "AND (@category_ids = {} OR category_ids = ANY(@category_ids))"
                " ORDER BY productid ASC LIMIT @limit OFFSET @offset;"
            )
        ),
        (
            "entity_with_enum_and_no_pk",
            ADDRESS_ENTITY,
            "SELECT street_address, city, state FROM address;",
        ),
        (
            "entity_with_sub_entity",
            CUSTOMER_ENTITY,
            "SELECT first_name, last_name, shipping_address_street_address, "
            "shipping_address_city, shipping_address_state, "
            "billing_address_street_address, billing_address_city, "
            "billing_address_state FROM customer;"
        )
    ])
    def test_gen_list_sql_statement(
        self, name: str, entity: Entity, expected_sql: str
    ):
        sql_gen = PgsqlCommandGenerator(entity)
        actual_sql = sql_gen.gen_list_sql_statement()
        self.assertEqual(expected_sql, actual_sql)

    @parameterized.expand([
        (
            "entity_with_no_ref",
            ENTITY_WITH_NO_REF,
            (
                "SELECT brand_id, name, description FROM Brand "
                "WHERE brand_id = @brand_id;"
            )
        ),
        (
            "entity_with_ref",
            ENTITY_WITH_REF,
            (
                "SELECT productid, name, description, price, quantity, "
                "brand_id, category_id FROM product "
                "WHERE productid = @productid;"
            )
        ),
        (
            "entity_with_enum_and_no_pk",
            ADDRESS_ENTITY,
            "SELECT street_address, city, state FROM address;"
        ),
        (
            "entity_with_sub_entity",
            CUSTOMER_ENTITY,
            "SELECT first_name, last_name, shipping_address_street_address, "
            "shipping_address_city, shipping_address_state, "
            "billing_address_street_address, billing_address_city, "
            "billing_address_state FROM customer;"
        )
    ])
    def test_gen_get_sql_statement(
        self, name: str, entity: Entity, expected_sql: str
    ):
        sql_gen = PgsqlCommandGenerator(entity)
        actual_sql = sql_gen.gen_get_sql_statement()
        self.assertEqual(expected_sql, actual_sql)

    @parameterized.expand([
        (
            "entity_with_no_ref",
            ENTITY_WITH_NO_REF,
            (
                "INSERT INTO Brand (brand_id, name, description) "
                "VALUES(@brand_id, @name, @description);"
            )
        ),
        (
            "entity_with_ref",
            ENTITY_WITH_REF,
            (
                "INSERT INTO product (productid, name, description, price, "
                "quantity, brand_id, category_id) "
                "VALUES(@productid, @name, @description, @price, @quantity, "
                "@brand_id, @category_id);"
            )
        ),
        (
            "entity_with_enum_and_no_pk",
            ADDRESS_ENTITY,
            (
                "INSERT INTO address (street_address, city, state) "
                "VALUES(@street_address, @city, @state);"
            )
        ),
        (
            "entity_with_sub_entity",
            CUSTOMER_ENTITY,
            "INSERT INTO customer (first_name, last_name, "
            "shipping_address_street_address, shipping_address_city, "
            "shipping_address_state, billing_address_street_address, "
            "billing_address_city, billing_address_state) "
            "VALUES(@first_name, @last_name, "
            "@shipping_address_street_address, @shipping_address_city, "
            "@shipping_address_state, @billing_address_street_address, "
            "@billing_address_city, @billing_address_state);"
        )
    ])
    def test_gen_create_sql_statement(
        self, name: str, entity: Entity, expected_sql: str
    ):
        sql_gen = PgsqlCommandGenerator(entity)
        actual_sql = sql_gen.gen_create_sql_statement()
        self.assertEqual(expected_sql, actual_sql)

    @parameterized.expand([
        (
            "entity_with_no_ref",
            ENTITY_WITH_NO_REF,
            (
                "UPDATE Brand  SET name = @name, description = @description "
                "WHERE brand_id = @brand_id;"
            )
        ),
        (
            "entity_with_ref",
            ENTITY_WITH_REF,
            (
                "UPDATE product  SET name = @name, description = @description,"
                " price = @price, quantity = @quantity, brand = @brand, "
                "category = @category WHERE productid = @productid;"
            )
        ),
        (
            "entity_with_enum_and_no_pk",
            ADDRESS_ENTITY,
            (
                "UPDATE address  SET street_address = @street_address, "
                "city = @city, state = @state;"
            )
        ),
        (
            "entity_with_sub_entity",
            CUSTOMER_ENTITY,
            "UPDATE customer  SET first_name = @first_name, "
            "last_name = @last_name, shipping_address = @shipping_address, "
            "billing_address = @billing_address;"
        )
    ])
    def test_gen_update_sql_statement(
        self, name: str, entity: Entity, expected_sql: str
    ):
        sql_gen = PgsqlCommandGenerator(entity)
        actual_sql = sql_gen.gen_update_sql_statement()
        self.assertEqual(expected_sql, actual_sql)

    @parameterized.expand([
        (
            "entity_with_no_ref",
            ENTITY_WITH_NO_REF,
            "DELETE FROM Brand WHERE brand_id = @brand_id;"
        ),
        (
            "entity_with_ref",
            ENTITY_WITH_REF,
            "DELETE FROM product WHERE productid = @productid;"
        ),
        (
            "entity_with_enum_and_no_pk",
            ADDRESS_ENTITY,
            "DELETE FROM address;"
        ),
        (
            "entity_with_sub_entity",
            CUSTOMER_ENTITY,
            "DELETE FROM customer;"
        )
    ])
    def test_gen_delete_sql_statement(
        self, name: str, entity: Entity, expected_sql: str
    ):
        sql_gen = PgsqlCommandGenerator(entity)
        actual_sql = sql_gen.gen_delete_sql_statement()
        self.assertEqual(expected_sql, actual_sql)


class TestPgsqlTableSqlGenerator(unittest.TestCase):
    def setUp(self):
        self.type_mapper = PgsqlTypeMapper()

    @parameterized.expand([
        (
            "entity_with_no_ref",
            ENTITY_WITH_NO_REF,
            [
                'CREATE TABLE IF NOT EXISTS Brand (',
                '    brand_id VARCHAR(30) PRIMARY KEY,',
                '    name VARCHAR(50) NOT NULL,',
                '    description VARCHAR(max) NULL',
                ');'
            ]
        ),
        (
            "entity_with_ref",
            ENTITY_WITH_REF,
            [
                'CREATE TABLE IF NOT EXISTS product (',
                '    productid VARCHAR(30) PRIMARY KEY,',
                '    name VARCHAR(50) NOT NULL,',
                '    description VARCHAR(max) NULL,',
                '    price DOUBLE NULL,',
                '    quantity INTEGER NULL,',
                '    brand_id VARCHAR(30) NOT NULL,',
                '    category_id INTEGER NOT NULL,',
                '    FOREIGN KEY (brand_id) REFERENCES Brand (brand_id),',
                '    FOREIGN KEY (category_id) REFERENCES Category (id)',
                ');'
            ]
        ),
        (
            "entity_with_enum_and_no_pk",
            ADDRESS_ENTITY,
            [
                'CREATE TABLE IF NOT EXISTS address (',
                '    street_address TEXT NOT NULL,',
                '    city TEXT NOT NULL,',
                '    state VARCHAR(50) NOT NULL',
                ');'
            ]
        ),
        (
            "entity_with_sub_entity",
            CUSTOMER_ENTITY,
            [
                'CREATE TABLE IF NOT EXISTS customer (',
                '    first_name TEXT NOT NULL,',
                '    last_name TEXT NOT NULL,',
                '    shipping_address_street_address TEXT NOT NULL,',
                '    shipping_address_city TEXT NOT NULL,',
                '    shipping_address_state VARCHAR(50) NOT NULL,',
                '    billing_address_street_address TEXT NOT NULL,',
                '    billing_address_city TEXT NOT NULL,',
                '    billing_address_state VARCHAR(50) NOT NULL',
                ');'
            ]
        ),
        (
            "entity_with_composite_key",
            COMPOSITE_PRIMARY_KEY_ENTITY,
            [
                'CREATE TABLE IF NOT EXISTS product_order (',
                '    order_id INTEGER,',
                '    product_id INTEGER,',
                '    quantity INTEGER NOT NULL,',
                '    price DOUBLE NOT NULL,',
                '    PRIMARY KEY (order_id, product_id)',
                ');'
            ]
        )
    ])
    def test_gen_table_sql(
        self, name: str, entity: Entity, expected_sql: List[str]
    ):
        tbl_sql_gen = PgsqlTableSqlGenerator()
        actual_sql = tbl_sql_gen.gen_table_sql(
            entity, self.type_mapper
        )
        self.assertEqual(expected_sql, actual_sql)
