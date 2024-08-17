import unittest

from entity_parser.entity import (
    Entity, EntityField, FieldFormat, FieldType, RefEntityField
)
from service_gens.csharp_service_gen.db_service_gen import (
    DbServiceGenerator, DbServiceUtil
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
SRC: str = "src"


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

ECOMMERCE_FILE_DATA = [
    FileData(
        file_path='output/path/Ecommerce/src/ProductDal/Interfaces',
        file_name='IDbService.cs',
        file_content=[
            'namespace ProductDal.Interfaces',
            '',
            '{',
            '    public interface IDbService',
            '    {',
            '        Task<int> ExecuteAsync'
            '(string sqlCommand, object? param);',
            '        Task<T?> GetAsync<T>(string sqlCommand, object? param);',
            '        Task<IEnumerable<T>> ListAsync<T>'
            '(string sqlCommand, object? param);',
            '    }',
            '}'
        ]
    ),
    FileData(
        file_path='output/path/Ecommerce/src/ProductDal/DbServices',
        file_name='DbService.cs',
        file_content=[
            'using System.Data;',
            'using Dapper;',
            'using ProductDal.Interfaces;',
            '',
            'namespace ProductDal.DbServices',
            '{',
            '    public class DbService(IDbConnection conn) : IDbService',
            '    {',
            '        public async Task<int> ExecuteAsync'
            '(string sqlCommand, object? param)',
            '        {',
            '       return await conn.ExecuteAsync(sqlCommand, param);',
            '        }',
            '',
            '        public async Task<T?> GetAsync<T>'
            '(string sqlCommand, object? param)',
            '        {',
            '       return await conn.QuerySingleOrDefaultAsync<T>'
            '(sqlCommand, param);',
            '        }',
            '',
            '        public async Task<IEnumerable<T>> ListAsync<T>'
            '(string sqlCommand, object? param)',
            '        {',
            '       return await conn.QueryAsync<T>(sqlCommand, param);',
            '        }',
            '    }',
            '}'
        ]
    ),
    FileData(
        file_path='output/path/Ecommerce/src/ProductDal/Interfaces',
        file_name='ISqlCommand.cs',
        file_content=[
            'namespace ProductDal.Interfaces',
            '{',
            '    public interface ISqlCommand',
            '    {',
            '        string GetCommand { get; }',
            '        string ListCommand { get; }',
            '        string CreateCommand { get; }',
            '        string UpdateCommand { get; }',
            '        string DeleteCommand { get; }',
            '    }',
            '}'
        ]
    ),
    FileData(
        file_path='output/path/Ecommerce/src/ProductDal/Interfaces',
        file_name='IBrandRepo.cs',
        file_content=[
            'using ProductDal.Models;',
            '',
            'namespace ProductDal.Interfaces',
            '{',
            '    public interface IBrandRepo',
            '    {',
            '        Task<Brand?> GetAsync(BrandGetParam brandGetParam);',
            '        Task<IEnumerable<Brand>> ListAsync'
            '(BrandListParam brandListParam);',
            '        Task<int> CreateAsync(Brand brand);',
            '        Task<int> UpdateAsync(Brand brand);',
            '        Task<int> DeleteAsync(BrandGetParam brandGetParam);',
            '    }',
            '}'
        ]
    ),
    FileData(
        file_path='output/path/Ecommerce/src/ProductDal/Models',
        file_name='BrandListParam.cs',
        file_content=[
            'namespace ProductDal.Models',
            '{',
            '    public class BrandListParam',
            '    {',
            '        public IEnumerable<string> brand_ids { get; set; } = '
            'default!;',
            '        public int Limit { get; set; } = 1000;',
            '        public int OffSet { get; set; } = 0;',
            '    }',
            '}'
        ]
    ),
    FileData(
        file_path='output/path/Ecommerce/src/ProductDal/Models',
        file_name='BrandGetParam.cs',
        file_content=[
            'namespace ProductDal.Models',
            '{',
            '    public class BrandGetParam',
            '    {',
            '        public string brand_id { get; set; } = default!;',
            '    }',
            '}'
        ]
    ),
    FileData(
        file_path='output/path/Ecommerce/src/ProductDal/Models',
        file_name='Brand.cs',
        file_content=[
            'namespace ProductDal.Models',
            '{',
            '    public class Brand',
            '    {',
            '        public string brand_id { get; set; } = default!;',
            '        public string name { get; set; } = default!;',
            '        public string? description { get; set; }',
            '    }',
            '}'
        ]
    ),
    FileData(
        file_path='output/path/Ecommerce/src/ProductDal/Interfaces',
        file_name='ICategoryRepo.cs',
        file_content=[
            'using ProductDal.Models;',
            '',
            'namespace ProductDal.Interfaces',
            '{',
            '    public interface ICategoryRepo',
            '    {',
            '        Task<Category?> GetAsync'
            '(CategoryGetParam categoryGetParam);',
            '        Task<IEnumerable<Category>> ListAsync'
            '(CategoryListParam categoryListParam);',
            '        Task<int> CreateAsync(Category category);',
            '        Task<int> UpdateAsync(Category category);',
            '        Task<int> DeleteAsync'
            '(CategoryGetParam categoryGetParam);',
            '    }',
            '}'
        ]
    ),
    FileData(
        file_path='output/path/Ecommerce/src/ProductDal/Models',
        file_name='CategoryListParam.cs',
        file_content=[
            'namespace ProductDal.Models',
            '{',
            '    public class CategoryListParam',
            '    {',
            '        public IEnumerable<int> ids { get; set; }',
            '        public int Limit { get; set; } = 1000;',
            '        public int OffSet { get; set; } = 0;',
            '    }',
            '}'
        ]
    ),
    FileData(
        file_path='output/path/Ecommerce/src/ProductDal/Models',
        file_name='CategoryGetParam.cs',
        file_content=[
            'namespace ProductDal.Models',
            '{',
            '    public class CategoryGetParam',
            '    {',
            '        public int id { get; set; }',
            '    }',
            '}'
        ]
    ),
    FileData(
        file_path='output/path/Ecommerce/src/ProductDal/Models',
        file_name='Category.cs',
        file_content=[
            'namespace ProductDal.Models',
            '{',
            '    public class Category',
            '    {',
            '        public int id { get; set; }',
            '        public string name { get; set; } = default!;',
            '        public string? description { get; set; }',
            '    }',
            '}'
        ]
    ),
    FileData(
        file_path='output/path/Ecommerce/src/ProductDal/Interfaces',
        file_name='IProductRepo.cs',
        file_content=[
            'using ProductDal.Models;',
            '',
            'namespace ProductDal.Interfaces',
            '{',
            '    public interface IProductRepo',
            '    {',
            '        Task<Product?> GetAsync'
            '(ProductGetParam productGetParam);',
            '        Task<IEnumerable<Product>> ListAsync'
            '(ProductListParam productListParam);',
            '        Task<int> CreateAsync(Product product);',
            '        Task<int> UpdateAsync(Product product);',
            '        Task<int> DeleteAsync(ProductGetParam productGetParam);',
            '    }',
            '}'
        ]
    ),
    FileData(
        file_path='output/path/Ecommerce/src/ProductDal/Models',
        file_name='ProductListParam.cs',
        file_content=[
            'namespace ProductDal.Models',
            '{',
            '    public class ProductListParam',
            '    {',
            '        public IEnumerable<Guid> productids { get; set; }',
            '        public int Limit { get; set; } = 1000;',
            '        public int OffSet { get; set; } = 0;',
            '    }',
            '}'
        ]
    ),
    FileData(
        file_path='output/path/Ecommerce/src/ProductDal/Models',
        file_name='ProductGetParam.cs',
        file_content=[
            'namespace ProductDal.Models',
            '{',
            '    public class ProductGetParam',
            '    {',
            '        public Guid productid { get; set; }',
            '    }',
            '}'
        ]
    ),
    FileData(
        file_path='output/path/Ecommerce/src/ProductDal/Models',
        file_name='Product.cs',
        file_content=[
            'namespace ProductDal.Models',
            '{',
            '    public class Product',
            '    {',
            '        public Guid productid { get; set; }',
            '        public string name { get; set; } = default!;',
            '        public string? description { get; set; }',
            '        public decimal? price { get; set; }',
            '        public int? quantity { get; set; }',
            '        public string brand_id { get; set; } = default!;',
            '        public int category_id { get; set; }',
            '    }',
            '}'
        ]
    )
]


class TestDbServiceGenerator(unittest.TestCase):
    def setUp(self) -> None:
        self.svc_dir = DbServiceUtil(
            output_path=OUTPUT_PATH,
            sln_name=ECOMMERCE,
            service_name=PRODUCT_DAL,
            src=SRC
        )

    def test_gen_service(self):
        service_gen = DbServiceGenerator(
            service_name=PRODUCT_DAL,
            svc_dir=self.svc_dir,
            entities=[BRAND_ENTITY, CATEGORY_ENTITY, PRODUCT_ENTITY],
            pl_type_mapper=CSharpTypeMapper(),
            db_type_mapper=None
        )
        actual_file_data = list(service_gen.gen_service())
        print(actual_file_data)
        self.assertEqual(ECOMMERCE_FILE_DATA, actual_file_data)
