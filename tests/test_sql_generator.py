import unittest
from parameterized import parameterized

from entity_parser.entity import Entity, EntityField, FieldType, RefEntityField
from sql_generator.sql_generator import PgsqlCommandGenerator

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
            "SELECT street_address, city, state FROM address;",
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
        )
    ])
    def test_gen_delete_sql_statement(
        self, name: str, entity: Entity, expected_sql: str
    ):
        sql_gen = PgsqlCommandGenerator(entity)
        actual_sql = sql_gen.gen_delete_sql_statement()
        self.assertEqual(expected_sql, actual_sql)
