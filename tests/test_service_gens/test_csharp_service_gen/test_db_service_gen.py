from typing import List
import unittest
from parameterized import parameterized

from entity_parser.entity import Entity, EntityField, FieldType, RefEntityField
from service_gens.csharp_service_gen.db_service_gen import (
    DbServiceModelGenerator
)
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
            format="uuid"
        )
    ]
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
            "        public IEnumerable<None> brand_ids { get; set; }",
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
            "        public None brand_id { get; set; }",
            "    }",
            "}"
        ]),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/Models",
        file_name="Brand.cs",
        file_content=[
            "namespace ProductDal.Models",
            "{",
            "    public class Brand",
            "    {",
            "        public None brand_id { get; set; }",
            "        public None name { get; set; }",
            "        public None description { get; set; }",
            "    }",
            "}"
        ]
    )
]

PRODUCT_FILE_DATA = [FileData(
    file_path='output/path/Ecommerce/src/ProductDal/Models',
    file_name='ListproductParam.cs',
    file_content=[
        'namespace ProductDal.Models',
        '{',
        '    public class ListproductParam',
        '    {',
        '        public IEnumerable<None> productids { get; set; }',
        '        public int Limit { get; set; } = 1000;',
        '        public int OffSet { get; set; } = 0;',
        '    }',
        '}'
    ]
),
    FileData(
    file_path='output/path/Ecommerce/src/ProductDal/Models',
    file_name='GetproductParam.cs',
    file_content=[
        'namespace ProductDal.Models',
        '{',
        '    public class GetproductParam',
        '    {',
        '        public None productid { get; set; }',
        '    }',
        '}'
    ]
),
    FileData(
    file_path='output/path/Ecommerce/src/ProductDal/Models',
    file_name='product.cs',
    file_content=[
        'namespace ProductDal.Models',
        '{',
        '    public class product',
        '    {',
        '        public None productid { get; set; }',
        '        public None name { get; set; }',
        '        public None description { get; set; }',
        '        public None price { get; set; }',
        '        public None quantity { get; set; }',
        '        public None brand_id { get; set; }',
        '        public None category_id { get; set; }',
        '    }',
        '}'
    ]
)]


class TestDbServiceModelGenerator(unittest.TestCase):
    def setUp(self) -> None:
        self.maxDiff = None

    @parameterized.expand([
        ("entity_with_pk", [BRAND_ENTITY], BRAND_FILE_DATA),
        ("entity_with_ref", [PRODUCT_ENTITY], PRODUCT_FILE_DATA)
    ])
    def test_entity_with_pk(
        self, name: str, entities: List[Entity], expected_data: FileData
    ):
        svc_gen = DbServiceModelGenerator(
            output_path=OUTPUT_PATH,
            sln_name="Ecommerce",
            service_name="ProductDal",
            entities=entities,
            pl_type_mapper=None,
            db_type_mapper=None
        )
        actual_data = []
        for svc in svc_gen.gen_service():
            for file_data in svc:
                actual_data.append(file_data)

        print(actual_data)
        self.assertEqual(expected_data, actual_data)
