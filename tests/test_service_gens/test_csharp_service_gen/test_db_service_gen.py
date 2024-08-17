from typing import List
import unittest
from parameterized import parameterized

from entity_parser.entity import (
    Entity, EntityField, FieldFormat, FieldType, RefEntityField
)
from service_gens.csharp_service_gen.db_service_gen import (
    DbServiceModelGenerator
)
from service_gens.service_gen import CSharpTypeMapper
from utils.utils import FileData

THIRTY: int = 30
FIFTY: int = 50

OUTPUT_PATH: str = "output/path"
ADDRESS: str = "address"
CATEGORY: str = "Category"
CITY: str = "city"
DESCRIPTION: str = "description"
MAX_LEN: str = "max"
NAME: str = "name"
STATE: str = "state"
STREET: str = "street"
ECOMMERCE: str = "Ecommerce"
PRODUCT_DAL: str = "ProductDal"

BRAND_ENTITY = Entity(
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

PRODUCT_ENTITY = Entity(
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
            format=FieldFormat.DECIMAL
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
            ref_entity=BRAND_ENTITY,
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
            format=FieldFormat.UUID
        )
    ]
)

DOT_NET_TYPE_ENTITY = Entity(
    name="DotNetDataTypes",
    non_ref_fields=[
        EntityField(
            name="BooleanField",
            is_required=True,
            field_type=FieldType.BOOLEAN,
            max_length=None,
            is_primary_key=False,
            type_ref=None,
            format=None,
            is_enum=False,
            enum_values=[],
            minimum=None,
            maximum=None
        ),
        EntityField(
            name="ByteField",
            is_required=True,
            field_type=FieldType.INTEGER,
            max_length=None,
            is_primary_key=False,
            type_ref=None,
            format=None,
            is_enum=False,
            enum_values=[],
            minimum=0,
            maximum=255
        ),
        EntityField(
            name="SByteField",
            is_required=True,
            field_type=FieldType.INTEGER,
            max_length=None,
            is_primary_key=False,
            type_ref=None,
            format=None,
            is_enum=False,
            enum_values=[],
            minimum=-128,
            maximum=127
        ),
        EntityField(
            name="CharField",
            is_required=True,
            field_type=FieldType.STRING,
            max_length=1,
            is_primary_key=False,
            type_ref=None,
            format=None,
            is_enum=False,
            enum_values=[],
            minimum=None,
            maximum=None
        ),
        EntityField(
            name="ShortField",
            is_required=True,
            field_type=FieldType.INTEGER,
            max_length=None,
            is_primary_key=False,
            type_ref=None,
            format=None,
            is_enum=False,
            enum_values=[],
            minimum=-32768,
            maximum=32767
        ),
        EntityField(
            name="UShortField",
            is_required=True,
            field_type=FieldType.INTEGER,
            max_length=None,
            is_primary_key=False,
            type_ref=None,
            format=None,
            is_enum=False,
            enum_values=[],
            minimum=0,
            maximum=65535
        ),
        EntityField(
            name="IntField",
            is_required=True,
            field_type=FieldType.INTEGER,
            max_length=None,
            is_primary_key=False,
            type_ref=None,
            format=None,
            is_enum=False,
            enum_values=[],
            minimum=-2147483648,
            maximum=2147483647
        ),
        EntityField(
            name="UIntField",
            is_required=True,
            field_type=FieldType.INTEGER,
            max_length=None,
            is_primary_key=False,
            type_ref=None,
            format=None,
            is_enum=False,
            enum_values=[],
            minimum=0,
            maximum=4294967295
        ),
        EntityField(
            name="LongField",
            is_required=True,
            field_type=FieldType.INTEGER,
            max_length=None,
            is_primary_key=False,
            type_ref=None,
            format=None,
            is_enum=False,
            enum_values=[],
            minimum=-9223372036854775808,
            maximum=9223372036854775807
        ),
        EntityField(
            name="ULongField",
            is_required=True,
            field_type=FieldType.INTEGER,
            max_length=None,
            is_primary_key=False,
            type_ref=None,
            format=None,
            is_enum=False,
            enum_values=[],
            minimum=0,
            maximum=18446744073709551615
        ),
        EntityField(
            name="FloatField",
            is_required=True,
            field_type=FieldType.NUMBER,
            max_length=None,
            is_primary_key=False,
            type_ref=None,
            format=FieldFormat.FLOAT,
            is_enum=False,
            enum_values=[],
            minimum=None,
            maximum=None
        ),
        EntityField(
            name="DoubleField",
            is_required=True,
            field_type=FieldType.NUMBER,
            max_length=None,
            is_primary_key=False,
            type_ref=None,
            format=FieldFormat.DOUBLE,
            is_enum=False,
            enum_values=[],
            minimum=None,
            maximum=None
        ),
        EntityField(
            name="DecimalField",
            is_required=True,
            field_type=FieldType.NUMBER,
            max_length=None,
            is_primary_key=False,
            type_ref=None,
            format=FieldFormat.DECIMAL,
            is_enum=False,
            enum_values=[],
            minimum=None,
            maximum=None
        ),
        EntityField(
            name="StringField",
            is_required=True,
            field_type=FieldType.STRING,
            max_length=None,
            is_primary_key=False,
            type_ref=None,
            format=None,
            is_enum=False,
            enum_values=[],
            minimum=None,
            maximum=None
        ),
        EntityField(
            name="DateTimeField",
            is_required=True,
            field_type=FieldType.STRING,
            max_length=None,
            is_primary_key=False,
            type_ref=None,
            format=FieldFormat.DATETIME,
            is_enum=False,
            enum_values=[],
            minimum=None,
            maximum=None
        ),
        EntityField(
            name="DateTimeOffField",
            is_required=True,
            field_type=FieldType.STRING,
            max_length=None,
            is_primary_key=False,
            type_ref=None,
            format=FieldFormat.DATETIME,
            is_enum=False,
            enum_values=[],
            minimum=None,
            maximum=None
        ),
        EntityField(
            name="EnumField",
            is_required=True,
            field_type=FieldType.STRING,
            max_length=None,
            is_primary_key=False,
            type_ref=None,
            format=None,
            is_enum=False,
            enum_values=[],
            minimum=None,
            maximum=None
        ),
        EntityField(
            name="GuidField",
            is_required=True,
            field_type=FieldType.STRING,
            max_length=None,
            is_primary_key=False,
            type_ref=None,
            format=FieldFormat.UUID,
            is_enum=False,
            enum_values=[],
            minimum=None,
            maximum=None
        ),
        EntityField(
            name="NullableGuidField",
            is_required=False,
            field_type=FieldType.STRING,
            max_length=None,
            is_primary_key=False,
            type_ref=None,
            format=FieldFormat.UUID,
            is_enum=False,
            enum_values=[],
            minimum=None,
            maximum=None
        ),
    ],
    ref_fields=[],
    pk_fields=[],
    is_enum=False,
    enum_values=None,
    is_sub_def=False
)

BRAND_FILE_DATA = [
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/Models",
        file_name="ListBrandParam.cs",
        file_content=[
            "namespace ProductDal.Models",
            "{",
            "    public class ListBrandParam",
            "    {",
            "        public IEnumerable<string> brand_ids { get; set; } "
            "= default!;",
            "        public int Limit { get; set; } = 1000;",
            "        public int OffSet { get; set; } = 0;",
            "    }",
            "}"
        ]
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/Models",
        file_name="GetBrandParam.cs",
        file_content=[
            "namespace ProductDal.Models",
            "{",
            "    public class GetBrandParam",
            "    {",
            "        public string brand_id { get; set; } = default!;",
            "    }",
            "}"
        ]
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/Models",
        file_name="Brand.cs",
        file_content=[
            "namespace ProductDal.Models",
            "{",
            "    public class Brand",
            "    {",
            "        public string brand_id { get; set; } = default!;",
            "        public string name { get; set; } = default!;",
            "        public string? description { get; set; }",
            "    }",
            "}"
        ]
    )
]

PRODUCT_FILE_DATA = [
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/Models",
        file_name="ListproductParam.cs",
        file_content=[
            "namespace ProductDal.Models",
            "{",
            "    public class ListproductParam",
            "    {",
            "        public IEnumerable<Guid> productids { get; set; }",
            "        public int Limit { get; set; } = 1000;",
            "        public int OffSet { get; set; } = 0;",
            "    }",
            "}"
        ]
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/Models",
        file_name="GetproductParam.cs",
        file_content=[
            "namespace ProductDal.Models",
            "{",
            "    public class GetproductParam",
            "    {",
            "        public Guid productid { get; set; }",
            "    }",
            "}"
        ]
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/Models",
        file_name="product.cs",
        file_content=[
            "namespace ProductDal.Models",
            "{",
            "    public class product",
            "    {",
            "        public Guid productid { get; set; }",
            "        public string name { get; set; } = default!;",
            "        public string? description { get; set; }",
            "        public decimal? price { get; set; }",
            "        public int? quantity { get; set; }",
            "        public string brand_id { get; set; } = default!;",
            "        public int category_id { get; set; }",
            "    }",
            "}"
        ]
    )
]

DOT_NET_ENTITY_TYPE_FILE_DATA = [
    FileData(
        file_path="",
        file_name="",
        file_content=[]
    ),
    FileData(
        file_path="",
        file_name="",
        file_content=[]
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/Models",
        file_name="DotNetDataTypes.cs",
        file_content=[
            "namespace ProductDal.Models",
            "{",
            "    public class DotNetDataTypes",
            "    {",
            "        public bool BooleanField { get; set; }",
            "        public byte ByteField { get; set; }",
            "        public sbyte SByteField { get; set; }",
            "        public string CharField { get; set; } = default!;",
            "        public short ShortField { get; set; }",
            "        public ushort UShortField { get; set; }",
            "        public int IntField { get; set; }",
            "        public uint UIntField { get; set; }",
            "        public long LongField { get; set; }",
            "        public ulong ULongField { get; set; }",
            "        public float FloatField { get; set; }",
            "        public double DoubleField { get; set; }",
            "        public decimal DecimalField { get; set; }",
            "        public string StringField { get; set; } = default!;",
            "        public DateTimeOffset DateTimeField { get; set; }",
            "        public DateTimeOffset DateTimeOffField { get; set; }",
            "        public string EnumField { get; set; } = default!;",
            "        public Guid GuidField { get; set; }",
            "        public Guid? NullableGuidField { get; set; }",
            "    }",
            "}"
        ]
    )
]


class TestDbServiceModelGenerator(unittest.TestCase):
    def setUp(self) -> None:
        self.maxDiff = None

    @ parameterized.expand([
        ("entity_with_pk", [BRAND_ENTITY], BRAND_FILE_DATA),
        ("entity_with_ref", [PRODUCT_ENTITY], PRODUCT_FILE_DATA),
        (
            "entity_with_dotnet_types",
            [DOT_NET_TYPE_ENTITY],
            DOT_NET_ENTITY_TYPE_FILE_DATA
        )
    ])
    def test_entity_with_pk(
        self, name: str, entities: List[Entity], expected_data: FileData
    ):
        svc_gen = DbServiceModelGenerator(
            output_path=OUTPUT_PATH,
            sln_name=ECOMMERCE,
            service_name=PRODUCT_DAL,
            entities=entities,
            pl_type_mapper=CSharpTypeMapper(),
            db_type_mapper=None
        )
        actual_data = [
            file_data
            for svc in svc_gen.gen_service()
            for file_data in svc
        ]
        print(actual_data)
        self.assertEqual(expected_data, actual_data)

    def test_gen_service(self):
        svc_gen = DbServiceModelGenerator(
            output_path=OUTPUT_PATH,
            sln_name=ECOMMERCE,
            service_name=PRODUCT_DAL,
            entities=[PRODUCT_ENTITY],
            pl_type_mapper=CSharpTypeMapper(),
            db_type_mapper=None
        )
        actual_data = [
            file_data
            for svc in svc_gen.gen_service()
            for file_data in svc
        ]
        print(actual_data)
        self.assertEqual(PRODUCT_FILE_DATA, actual_data)
