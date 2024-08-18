from typing import List
import unittest
from parameterized import parameterized

from entity_parser.entity import (
    Entity, EntityField, FieldFormat, FieldType, RefEntityField
)
from service_gens.csharp_service_gen.db_service_gen import (
    DbServiceGenerator, DbServiceUtil
)
from service_gens.service_gen import CSharpTypeMapper
from sql_generator.sql_generator import PgsqlCommandGenerator
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
        file_path="output/path/Ecommerce/src/ProductDal/Interfaces",
        file_name="IDbService.cs",
        file_content=[
            "namespace ProductDal.Interfaces",
            "",
            "{",
            "    public interface IDbService",
            "    {",
            "        Task<int> ExecuteAsync"
            "(string sqlCommand, object? param);",
            "        Task<T?> GetAsync<T>(string sqlCommand, object? param);",
            "        Task<IEnumerable<T>> ListAsync<T>"
            "(string sqlCommand, object? param);",
            "    }",
            "}",
        ],
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/DbServices",
        file_name="DbService.cs",
        file_content=[
            "using System.Data;",
            "using Dapper;",
            "using ProductDal.Interfaces;",
            "",
            "namespace ProductDal.DbServices",
            "{",
            "    public class DbService(IDbConnection conn) : IDbService",
            "    {",
            "        public async Task<int> ExecuteAsync"
            "(string sqlCommand, object? param)",
            "        {",
            "           return await conn.ExecuteAsync(sqlCommand, param);",
            "        }",
            "",
            "        public async Task<T?> GetAsync<T>"
            "(string sqlCommand, object? param)",
            "        {",
            "           return await conn.QuerySingleOrDefaultAsync<T>"
            "(sqlCommand, param);",
            "        }",
            "",
            "        public async Task<IEnumerable<T>> ListAsync<T>"
            "(string sqlCommand, object? param)",
            "        {",
            "           return await conn.QueryAsync<T>(sqlCommand, param);",
            "        }",
            "    }",
            "}",
        ],
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/Interfaces",
        file_name="ISqlCommand.cs",
        file_content=[
            "namespace ProductDal.Interfaces",
            "{",
            "    public interface ISqlCommand",
            "    {",
            "        string GetCommand { get; }",
            "        string ListCommand { get; }",
            "        string CreateCommand { get; }",
            "        string UpdateCommand { get; }",
            "        string DeleteCommand { get; }",
            "    }",
            "}",
        ],
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/Interfaces",
        file_name="IBrandRepo.cs",
        file_content=[
            "using ProductDal.Models;",
            "",
            "namespace ProductDal.Interfaces",
            "{",
            "    public interface IBrandRepo",
            "    {",
            "        Task<Brand?> GetAsync(BrandGetParam brandGetParam);",
            "        Task<IEnumerable<Brand>> ListAsync"
            "(BrandListParam brandListParam);",
            "        Task<int> CreateAsync(Brand brand);",
            "        Task<int> UpdateAsync(Brand brand);",
            "        Task<int> DeleteAsync(BrandGetParam brandGetParam);",
            "    }",
            "}",
        ],
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/Models",
        file_name="BrandListParam.cs",
        file_content=[
            "namespace ProductDal.Models",
            "{",
            "    public class BrandListParam",
            "    {",
            "        public IEnumerable<string> brand_ids { get; set; } = "
            "default!;",
            "        public int Limit { get; set; } = 1000;",
            "        public int OffSet { get; set; } = 0;",
            "    }",
            "}",
        ],
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/Models",
        file_name="BrandGetParam.cs",
        file_content=[
            "namespace ProductDal.Models",
            "{",
            "    public class BrandGetParam",
            "    {",
            "        public string brand_id { get; set; } = default!;",
            "    }",
            "}",
        ],
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
            "}",
        ],
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/SqlCommands",
        file_name="BrandSqlCommand.cs",
        file_content=[
            "using ProductDal.Interfaces",
            "",
            "namespace ProductDal.Interfaces",
            "{",
            "public class BrandSqlCommand : ISqlCommand",
            "    {",
            '        public string GetCommand => "SELECT brand_id, name, '
            'description FROM Brand WHERE brand_id = @brand_id;"',
            '        public string ListCommand => "SELECT brand_id, name, '
            'description FROM Brand '
            'WHERE (@brand_ids = {} OR brand_ids = ANY(@brand_ids)) '
            'ORDER BY brand_id ASC LIMIT @limit OFFSET @offset;"',
            '        public string CreateCommand => "INSERT INTO Brand'
            '(brand_id, name, description) '
            'VALUES(@brand_id, @name, @description);"',
            '        public string UpdateCommand => "UPDATE Brand  '
            'SET name = @name, description = @description '
            'WHERE brand_id = @brand_id;"',
            '        public string DeleteCommand => "DELETE FROM Brand '
            'WHERE brand_id = @brand_id;"',
            "    }",
            "}",
        ],
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/Repos",
        file_name="BrandRepo.cs",
        file_content=[
            "using ProductDal.Interfaces",
            "using ProductDal.Models",
            "",
            "namespace ProductDal.Repos",
            "{",
            "public class BrandRepo(IDbService DbService, "
            "ISqlCommand sqlCommand) : IBrand",
            "    {",
            "        public async Task<Brand?> GetAsync"
            "(BrandGetParam brandGetParam)",
            "        {",
            "           return await DbService.GetAsync<Brand>"
            "(sqlCommand.GetCommand, brandGetParam);",
            "        }",
            "",
            "         public async Task<IEnumerable<Brand>> ListAsync"
            "(BrandListParam brand)",
            "        {",
            "           return await dbService.ListAsync<Brand>"
            "(sqlCommand.ListCommand, brand);",
            "        }",
            "",
            "        public async Task<int> CreateAsync(Brand brand)",
            "        {",
            "           return await dbService.ExecuteAsync"
            "(sqlCommand.CreateCommand, brand);",
            "        }",
            "",
            "        public async Task<int> UpdateAsync(Brand brand)",
            "        {",
            "           return await dbService.ExecuteAsync"
            "(sqlCommand.UpdateCommand, brand);",
            "        }",
            "",
            "        public async Task<int> DeleteAsync"
            "(BrandGetParam brandGetParam)",
            "        {",
            "           return await dbService.ExecuteAsync"
            "(sqlCommand.DeleteCommand, brandGetParam);",
            "        }",
            "    }",
            "}",
        ],
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/Interfaces",
        file_name="ICategoryRepo.cs",
        file_content=[
            "using ProductDal.Models;",
            "",
            "namespace ProductDal.Interfaces",
            "{",
            "    public interface ICategoryRepo",
            "    {",
            "        Task<Category?> GetAsync"
            "(CategoryGetParam categoryGetParam);",
            "        Task<IEnumerable<Category>> ListAsync"
            "(CategoryListParam categoryListParam);",
            "        Task<int> CreateAsync(Category category);",
            "        Task<int> UpdateAsync(Category category);",
            "        Task<int> DeleteAsync"
            "(CategoryGetParam categoryGetParam);",
            "    }",
            "}",
        ],
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/Models",
        file_name="CategoryListParam.cs",
        file_content=[
            "namespace ProductDal.Models",
            "{",
            "    public class CategoryListParam",
            "    {",
            "        public IEnumerable<int> ids { get; set; }",
            "        public int Limit { get; set; } = 1000;",
            "        public int OffSet { get; set; } = 0;",
            "    }",
            "}",
        ],
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/Models",
        file_name="CategoryGetParam.cs",
        file_content=[
            "namespace ProductDal.Models",
            "{",
            "    public class CategoryGetParam",
            "    {",
            "        public int id { get; set; }",
            "    }",
            "}",
        ],
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/Models",
        file_name="Category.cs",
        file_content=[
            "namespace ProductDal.Models",
            "{",
            "    public class Category",
            "    {",
            "        public int id { get; set; }",
            "        public string name { get; set; } = default!;",
            "        public string? description { get; set; }",
            "    }",
            "}",
        ],
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/SqlCommands",
        file_name="CategorySqlCommand.cs",
        file_content=[
            "using ProductDal.Interfaces",
            "",
            "namespace ProductDal.Interfaces",
            "{",
            "public class CategorySqlCommand : ISqlCommand",
            "    {",
            '        public string GetCommand => "SELECT id, name, '
            'description FROM Category WHERE id = @id;"',
            '        public string ListCommand => "SELECT id, name, '
            'description FROM Category WHERE (@ids = {} OR ids = ANY(@ids)) '
            'ORDER BY id ASC LIMIT @limit OFFSET @offset;"',
            '        public string CreateCommand => "INSERT INTO Category'
            '(id, name, description) VALUES(@id, @name, @description);"',
            '        public string UpdateCommand => "UPDATE Category  '
            'SET name = @name, description = @description WHERE id = @id;"',
            '        public string DeleteCommand => "DELETE FROM Category '
            'WHERE id = @id;"',
            "    }",
            "}",
        ],
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/Repos",
        file_name="CategoryRepo.cs",
        file_content=[
            "using ProductDal.Interfaces",
            "using ProductDal.Models",
            "",
            "namespace ProductDal.Repos",
            "{",
            "public class CategoryRepo(IDbService DbService, "
            "ISqlCommand sqlCommand) : ICategory",
            "    {",
            "        public async Task<Brand?> GetAsync"
            "(CategoryGetParam categoryGetParam)",
            "        {",
            "           return await DbService.GetAsync<Category>"
            "(sqlCommand.GetCommand, categoryGetParam);",
            "        }",
            "",
            "         public async Task<IEnumerable<Category>> ListAsync"
            "(CategoryListParam category)",
            "        {",
            "           return await dbService.ListAsync<Category>"
            "(sqlCommand.ListCommand, category);",
            "        }",
            "",
            "        public async Task<int> CreateAsync(Category category)",
            "        {",
            "           return await dbService.ExecuteAsync"
            "(sqlCommand.CreateCommand, category);",
            "        }",
            "",
            "        public async Task<int> UpdateAsync(Category category)",
            "        {",
            "           return await dbService.ExecuteAsync"
            "(sqlCommand.UpdateCommand, category);",
            "        }",
            "",
            "        public async Task<int> DeleteAsync"
            "(CategoryGetParam categoryGetParam)",
            "        {",
            "           return await dbService.ExecuteAsync"
            "(sqlCommand.DeleteCommand, categoryGetParam);",
            "        }",
            "    }",
            "}",
        ],
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/Interfaces",
        file_name="IProductRepo.cs",
        file_content=[
            "using ProductDal.Models;",
            "",
            "namespace ProductDal.Interfaces",
            "{",
            "    public interface IProductRepo",
            "    {",
            "        Task<Product?> GetAsync"
            "(ProductGetParam productGetParam);",
            "        Task<IEnumerable<Product>> ListAsync"
            "(ProductListParam productListParam);",
            "        Task<int> CreateAsync(Product product);",
            "        Task<int> UpdateAsync(Product product);",
            "        Task<int> DeleteAsync(ProductGetParam productGetParam);",
            "    }",
            "}",
        ],
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/Models",
        file_name="ProductListParam.cs",
        file_content=[
            "namespace ProductDal.Models",
            "{",
            "    public class ProductListParam",
            "    {",
            "        public IEnumerable<Guid> productids { get; set; }",
            "        public int Limit { get; set; } = 1000;",
            "        public int OffSet { get; set; } = 0;",
            "    }",
            "}",
        ],
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/Models",
        file_name="ProductGetParam.cs",
        file_content=[
            "namespace ProductDal.Models",
            "{",
            "    public class ProductGetParam",
            "    {",
            "        public Guid productid { get; set; }",
            "    }",
            "}",
        ],
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/Models",
        file_name="Product.cs",
        file_content=[
            "namespace ProductDal.Models",
            "{",
            "    public class Product",
            "    {",
            "        public Guid productid { get; set; }",
            "        public string name { get; set; } = default!;",
            "        public string? description { get; set; }",
            "        public decimal? price { get; set; }",
            "        public int? quantity { get; set; }",
            "        public string brand_id { get; set; } = default!;",
            "        public int category_id { get; set; }",
            "    }",
            "}",
        ],
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/SqlCommands",
        file_name="ProductSqlCommand.cs",
        file_content=[
            "using ProductDal.Interfaces",
            "",
            "namespace ProductDal.Interfaces",
            "{",
            "public class ProductSqlCommand : ISqlCommand",
            "    {",
            '        public string GetCommand => "SELECT productid, name, '
            'description, price, quantity, brand_id, category_id FROM product '
            'WHERE productid = @productid;"',
            '        public string ListCommand => "SELECT productid, name, '
            'description, price, quantity, brand_id, category_id FROM product '
            'WHERE (@productids = {} OR productids = ANY(@productids)) AND '
            '(@brand_ids = {} OR brand_ids = ANY(@brand_ids)) AND '
            '(@category_ids = {} OR category_ids = ANY(@category_ids)) ORDER '
            'BY productid ASC LIMIT @limit OFFSET @offset;"',
            '        public string CreateCommand => "INSERT INTO product'
            '(productid, name, description, price, quantity, brand_id, '
            'category_id) VALUES(@productid, @name, @description, @price, '
            '@quantity, @brand_id, @category_id);"',
            '        public string UpdateCommand => "UPDATE product  '
            'SET name = @name, description = @description, price = @price, '
            'quantity = @quantity, brand_id = @brand_id, category_id = '
            '@category_id WHERE productid = @productid;"',
            '        public string DeleteCommand => "DELETE FROM product '
            'WHERE productid = @productid;"',
            "    }",
            "}",
        ],
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/Repos",
        file_name="ProductRepo.cs",
        file_content=[
            "using ProductDal.Interfaces",
            "using ProductDal.Models",
            "",
            "namespace ProductDal.Repos",
            "{",
            "public class ProductRepo(IDbService DbService, "
            "ISqlCommand sqlCommand) : IProduct",
            "    {",
            "        public async Task<Brand?> GetAsync"
            "(ProductGetParam productGetParam)",
            "        {",
            "           return await DbService.GetAsync<Product>"
            "(sqlCommand.GetCommand, productGetParam);",
            "        }",
            "",
            "         public async Task<IEnumerable<Product>> ListAsync"
            "(ProductListParam product)",
            "        {",
            "           return await dbService.ListAsync<Product>"
            "(sqlCommand.ListCommand, product);",
            "        }",
            "",
            "        public async Task<int> CreateAsync(Product product)",
            "        {",
            "           return await dbService.ExecuteAsync"
            "(sqlCommand.CreateCommand, product);",
            "        }",
            "",
            "        public async Task<int> UpdateAsync(Product product)",
            "        {",
            "           return await dbService.ExecuteAsync"
            "(sqlCommand.UpdateCommand, product);",
            "        }",
            "",
            "        public async Task<int> DeleteAsync"
            "(ProductGetParam productGetParam)",
            "        {",
            "           return await dbService.ExecuteAsync"
            "(sqlCommand.DeleteCommand, productGetParam);",
            "        }",
            "    }",
            "}",
        ],
    ),
]

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

DOTNET_TYPE_ENTITY_FILE_DATA = [
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/Interfaces",
        file_name="IDbService.cs",
        file_content=[
            "namespace ProductDal.Interfaces",
            "",
            "{",
            "    public interface IDbService",
            "    {",
            "        Task<int> ExecuteAsync"
            "(string sqlCommand, object? param);",
            "        Task<T?> GetAsync<T>(string sqlCommand, object? param);",
            "        Task<IEnumerable<T>> ListAsync<T>"
            "(string sqlCommand, object? param);",
            "    }",
            "}",
        ],
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/DbServices",
        file_name="DbService.cs",
        file_content=[
            "using System.Data;",
            "using Dapper;",
            "using ProductDal.Interfaces;",
            "",
            "namespace ProductDal.DbServices",
            "{",
            "    public class DbService(IDbConnection conn) : IDbService",
            "    {",
            "        public async Task<int> ExecuteAsync"
            "(string sqlCommand, object? param)",
            "        {",
            "           return await conn.ExecuteAsync(sqlCommand, param);",
            "        }",
            "",
            "        public async Task<T?> GetAsync<T>"
            "(string sqlCommand, object? param)",
            "        {",
            "           return await conn.QuerySingleOrDefaultAsync<T>"
            "(sqlCommand, param);",
            "        }",
            "",
            "        public async Task<IEnumerable<T>> ListAsync<T>"
            "(string sqlCommand, object? param)",
            "        {",
            "           return await conn.QueryAsync<T>(sqlCommand, param);",
            "        }",
            "    }",
            "}",
        ],
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/Interfaces",
        file_name="ISqlCommand.cs",
        file_content=[
            "namespace ProductDal.Interfaces",
            "{",
            "    public interface ISqlCommand",
            "    {",
            "        string GetCommand { get; }",
            "        string ListCommand { get; }",
            "        string CreateCommand { get; }",
            "        string UpdateCommand { get; }",
            "        string DeleteCommand { get; }",
            "    }",
            "}",
        ],
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/Interfaces",
        file_name="IDotNetDataTypesRepo.cs",
        file_content=[
            "using ProductDal.Models;",
            "",
            "namespace ProductDal.Interfaces",
            "{",
            "    public interface IDotNetDataTypesRepo",
            "    {",
            "        Task<DotNetDataTypes?> GetAsync"
            "(DotNetDataTypesGetParam dotNetDataTypesGetParam);",
            "        Task<IEnumerable<DotNetDataTypes>> ListAsync"
            "(DotNetDataTypesListParam dotNetDataTypesListParam);",
            "        Task<int> CreateAsync(DotNetDataTypes dotNetDataTypes);",
            "        Task<int> UpdateAsync(DotNetDataTypes dotNetDataTypes);",
            "        Task<int> DeleteAsync"
            "(DotNetDataTypesGetParam dotNetDataTypesGetParam);",
            "    }",
            "}",
        ],
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/Models",
        file_name="DotNetDataTypesListParam.cs",
        file_content=[
            "namespace ProductDal.Models",
            "{",
            "    public class DotNetDataTypesListParam",
            "    {",
            "        public int Limit { get; set; } = 1000;",
            "        public int OffSet { get; set; } = 0;",
            "    }",
            "}",
        ],
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/Models",
        file_name="DotNetDataTypesGetParam.cs",
        file_content=[
            "namespace ProductDal.Models",
            "{",
            "    public class DotNetDataTypesGetParam",
            "    {",
            "    }",
            "}",
        ],
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
            "}",
        ],
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/SqlCommands",
        file_name="DotNetDataTypesSqlCommand.cs",
        file_content=[
            "using ProductDal.Interfaces",
            "",
            "namespace ProductDal.Interfaces",
            "{",
            "public class DotNetDataTypesSqlCommand : ISqlCommand",
            "    {",
            '        public string GetCommand => "SELECT BooleanField, '
            'ByteField, SByteField, CharField, ShortField, UShortField, '
            'IntField, UIntField, LongField, ULongField, FloatField, '
            'DoubleField, DecimalField, StringField, DateTimeField, '
            'DateTimeOffField, EnumField, GuidField, NullableGuidField '
            'FROM DotNetDataTypes;"',
            '        public string ListCommand => "SELECT BooleanField, '
            'ByteField, SByteField, CharField, ShortField, UShortField, '
            'IntField, UIntField, LongField, ULongField, FloatField, '
            'DoubleField, DecimalField, StringField, DateTimeField, '
            'DateTimeOffField, EnumField, GuidField, NullableGuidField '
            'FROM DotNetDataTypes;"',
            '        public string CreateCommand => '
            '"INSERT INTO DotNetDataTypes(BooleanField, ByteField, '
            'SByteField, CharField, ShortField, UShortField, IntField, '
            'UIntField, LongField, ULongField, FloatField, DoubleField, '
            'DecimalField, StringField, DateTimeField, DateTimeOffField, '
            'EnumField, GuidField, NullableGuidField) VALUES(@BooleanField, '
            '@ByteField, @SByteField, @CharField, @ShortField, @UShortField, '
            '@IntField, @UIntField, @LongField, @ULongField, @FloatField, '
            '@DoubleField, @DecimalField, @StringField, @DateTimeField, '
            '@DateTimeOffField, @EnumField, @GuidField, @NullableGuidField);"',
            '        public string UpdateCommand => '
            '"UPDATE DotNetDataTypes  SET BooleanField = @BooleanField, '
            'ByteField = @ByteField, SByteField = @SByteField, '
            'CharField = @CharField, ShortField = @ShortField, '
            'UShortField = @UShortField, IntField = @IntField, '
            'UIntField = @UIntField, LongField = @LongField, '
            'ULongField = @ULongField, FloatField = @FloatField, '
            'DoubleField = @DoubleField, DecimalField = @DecimalField, '
            'StringField = @StringField, DateTimeField = @DateTimeField, '
            'DateTimeOffField = @DateTimeOffField, EnumField = @EnumField, '
            'GuidField = @GuidField, NullableGuidField = @NullableGuidField;"',
            '        public string DeleteCommand '
            '=> "DELETE FROM DotNetDataTypes;"',
            "    }",
            "}",
        ],
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/Repos",
        file_name="DotNetDataTypesRepo.cs",
        file_content=[
            "using ProductDal.Interfaces",
            "using ProductDal.Models",
            "",
            "namespace ProductDal.Repos",
            "{",
            "public class DotNetDataTypesRepo(IDbService DbService, "
            "ISqlCommand sqlCommand) : IDotNetDataTypes",
            "    {",
            "        public async Task<Brand?> GetAsync"
            "(DotNetDataTypesGetParam dotNetDataTypesGetParam)",
            "        {",
            "           return await DbService.GetAsync<DotNetDataTypes>"
            "(sqlCommand.GetCommand, dotNetDataTypesGetParam);",
            "        }",
            "",
            "         public async Task<IEnumerable<DotNetDataTypes>> "
            "ListAsync(DotNetDataTypesListParam dotNetDataTypes)",
            "        {",
            "           return await dbService.ListAsync<DotNetDataTypes>"
            "(sqlCommand.ListCommand, dotNetDataTypes);",
            "        }",
            "",
            "        public async Task<int> CreateAsync"
            "(DotNetDataTypes dotNetDataTypes)",
            "        {",
            "           return await dbService.ExecuteAsync"
            "(sqlCommand.CreateCommand, dotNetDataTypes);",
            "        }",
            "",
            "        public async Task<int> UpdateAsync"
            "(DotNetDataTypes dotNetDataTypes)",
            "        {",
            "           return await dbService.ExecuteAsync"
            "(sqlCommand.UpdateCommand, dotNetDataTypes);",
            "        }",
            "",
            "        public async Task<int> DeleteAsync"
            "(DotNetDataTypesGetParam dotNetDataTypesGetParam)",
            "        {",
            "           return await dbService.ExecuteAsync"
            "(sqlCommand.DeleteCommand, dotNetDataTypesGetParam);",
            "        }",
            "    }",
            "}",
        ],
    ),
]

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

CUSTOMER_ADDRESS_ENTITY_FILE_DATA = [
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/Interfaces",
        file_name="IDbService.cs",
        file_content=[
            "namespace ProductDal.Interfaces",
            "",
            "{",
            "    public interface IDbService",
            "    {",
            "        Task<int> ExecuteAsync"
            "(string sqlCommand, object? param);",
            "        Task<T?> GetAsync<T>"
            "(string sqlCommand, object? param);",
            "        Task<IEnumerable<T>> ListAsync<T>"
            "(string sqlCommand, object? param);",
            "    }",
            "}",
        ],
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/DbServices",
        file_name="DbService.cs",
        file_content=[
            "using System.Data;",
            "using Dapper;",
            "using ProductDal.Interfaces;",
            "",
            "namespace ProductDal.DbServices",
            "{",
            "    public class DbService(IDbConnection conn) : IDbService",
            "    {",
            "        public async Task<int> ExecuteAsync"
            "(string sqlCommand, object? param)",
            "        {",
            "           return await conn.ExecuteAsync(sqlCommand, param);",
            "        }",
            "",
            "        public async Task<T?> GetAsync<T>"
            "(string sqlCommand, object? param)",
            "        {",
            "           return await conn.QuerySingleOrDefaultAsync<T>"
            "(sqlCommand, param);",
            "        }",
            "",
            "        public async Task<IEnumerable<T>> ListAsync<T>"
            "(string sqlCommand, object? param)",
            "        {",
            "           return await conn.QueryAsync<T>(sqlCommand, param);",
            "        }",
            "    }",
            "}",
        ],
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/Interfaces",
        file_name="ISqlCommand.cs",
        file_content=[
            "namespace ProductDal.Interfaces",
            "{",
            "    public interface ISqlCommand",
            "    {",
            "        string GetCommand { get; }",
            "        string ListCommand { get; }",
            "        string CreateCommand { get; }",
            "        string UpdateCommand { get; }",
            "        string DeleteCommand { get; }",
            "    }",
            "}",
        ],
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/Interfaces",
        file_name="IAddressRepo.cs",
        file_content=[
            "using ProductDal.Models;",
            "",
            "namespace ProductDal.Interfaces",
            "{",
            "    public interface IAddressRepo",
            "    {",
            "        Task<Address?> GetAsync"
            "(AddressGetParam addressGetParam);",
            "        Task<IEnumerable<Address>> ListAsync"
            "(AddressListParam addressListParam);",
            "        Task<int> CreateAsync(Address address);",
            "        Task<int> UpdateAsync(Address address);",
            "        Task<int> DeleteAsync(AddressGetParam addressGetParam);",
            "    }",
            "}",
        ],
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/Models",
        file_name="AddressListParam.cs",
        file_content=[
            "namespace ProductDal.Models",
            "{",
            "    public class AddressListParam",
            "    {",
            "        public int Limit { get; set; } = 1000;",
            "        public int OffSet { get; set; } = 0;",
            "    }",
            "}",
        ],
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/Models",
        file_name="AddressGetParam.cs",
        file_content=[
            "namespace ProductDal.Models",
            "{",
            "    public class AddressGetParam",
            "    {",
            "    }",
            "}",
        ],
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/Models",
        file_name="Address.cs",
        file_content=[
            "namespace ProductDal.Models",
            "{",
            "    public class Address",
            "    {",
            "        public string street_address { get; set; } = default!;",
            "        public string city { get; set; } = default!;",
            "        public CSharpDataType.STRING state { get; set; }",
            "    }",
            "}",
        ],
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/SqlCommands",
        file_name="AddressSqlCommand.cs",
        file_content=[
            "using ProductDal.Interfaces",
            "",
            "namespace ProductDal.Interfaces",
            "{",
            "public class AddressSqlCommand : ISqlCommand",
            "    {",
            '        public string GetCommand => '
            '"SELECT street_address, city, state FROM address;"',
            '        public string ListCommand => '
            '"SELECT street_address, city, state FROM address;"',
            '        public string CreateCommand => '
            '"INSERT INTO address(street_address, city, state) '
            'VALUES(@street_address, @city, @state);"',
            '        public string UpdateCommand => '
            '"UPDATE address  SET street_address = @street_address, '
            'city = @city, state = @state;"',
            '        public string DeleteCommand => "DELETE FROM address;"',
            "    }",
            "}",
        ],
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/Repos",
        file_name="AddressRepo.cs",
        file_content=[
            "using ProductDal.Interfaces",
            "using ProductDal.Models",
            "",
            "namespace ProductDal.Repos",
            "{",
            "public class AddressRepo"
            "(IDbService DbService, ISqlCommand sqlCommand) : IAddress",
            "    {",
            "        public async Task<Brand?> GetAsync"
            "(AddressGetParam addressGetParam)",
            "        {",
            "           return await DbService.GetAsync<Address>"
            "(sqlCommand.GetCommand, addressGetParam);",
            "        }",
            "",
            "         public async Task<IEnumerable<Address>> ListAsync"
            "(AddressListParam address)",
            "        {",
            "           return await dbService.ListAsync<Address>"
            "(sqlCommand.ListCommand, address);",
            "        }",
            "",
            "        public async Task<int> CreateAsync(Address address)",
            "        {",
            "           return await dbService.ExecuteAsync"
            "(sqlCommand.CreateCommand, address);",
            "        }",
            "",
            "        public async Task<int> UpdateAsync(Address address)",
            "        {",
            "           return await dbService.ExecuteAsync"
            "(sqlCommand.UpdateCommand, address);",
            "        }",
            "",
            "        public async Task<int> DeleteAsync"
            "(AddressGetParam addressGetParam)",
            "        {",
            "           return await dbService.ExecuteAsync"
            "(sqlCommand.DeleteCommand, addressGetParam);",
            "        }",
            "    }",
            "}",
        ],
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/Interfaces",
        file_name="ICustomerRepo.cs",
        file_content=[
            "using ProductDal.Models;",
            "",
            "namespace ProductDal.Interfaces",
            "{",
            "    public interface ICustomerRepo",
            "    {",
            "        Task<Customer?> GetAsync"
            "(CustomerGetParam customerGetParam);",
            "        Task<IEnumerable<Customer>> ListAsync"
            "(CustomerListParam customerListParam);",
            "        Task<int> CreateAsync(Customer customer);",
            "        Task<int> UpdateAsync(Customer customer);",
            "        Task<int> DeleteAsync"
            "(CustomerGetParam customerGetParam);",
            "    }",
            "}",
        ],
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/Models",
        file_name="CustomerListParam.cs",
        file_content=[
            "namespace ProductDal.Models",
            "{",
            "    public class CustomerListParam",
            "    {",
            "        public int Limit { get; set; } = 1000;",
            "        public int OffSet { get; set; } = 0;",
            "    }",
            "}",
        ],
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/Models",
        file_name="CustomerGetParam.cs",
        file_content=[
            "namespace ProductDal.Models",
            "{",
            "    public class CustomerGetParam",
            "    {",
            "    }",
            "}",
        ],
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/Models",
        file_name="Customer.cs",
        file_content=[
            "namespace ProductDal.Models",
            "{",
            "    public class Customer",
            "    {",
            "        public string first_name { get; set; } = default!;",
            "        public string last_name { get; set; } = default!;",
            "        public string shipping_address_street_address "
            "{ get; set; } = default!;",
            "        public string shipping_address_city { get; set; } = "
            "default!;",
            "        public CSharpDataType.STRING shipping_address_state "
            "{ get; set; }",
            "        public string billing_address_street_address "
            "{ get; set; } = default!;",
            "        public string billing_address_city { get; set; } = "
            "default!;",
            "        public CSharpDataType.STRING billing_address_state "
            "{ get; set; }",
            "    }",
            "}",
        ],
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/SqlCommands",
        file_name="CustomerSqlCommand.cs",
        file_content=[
            "using ProductDal.Interfaces",
            "",
            "namespace ProductDal.Interfaces",
            "{",
            "public class CustomerSqlCommand : ISqlCommand",
            "    {",
            '        public string GetCommand => "SELECT first_name, '
            'last_name, shipping_address_street_address, '
            'shipping_address_city, shipping_address_state, '
            'billing_address_street_address, billing_address_city, '
            'billing_address_state FROM customer;"',
            '        public string ListCommand => "SELECT first_name, '
            'last_name, shipping_address_street_address, '
            'shipping_address_city, shipping_address_state, '
            'billing_address_street_address, billing_address_city, '
            'billing_address_state FROM customer;"',
            '        public string CreateCommand => "INSERT INTO customer'
            '(first_name, last_name, shipping_address_street_address, '
            'shipping_address_city, shipping_address_state, '
            'billing_address_street_address, billing_address_city, '
            'billing_address_state) VALUES(@first_name, @last_name, '
            '@shipping_address_street_address, @shipping_address_city, '
            '@shipping_address_state, @billing_address_street_address, '
            '@billing_address_city, @billing_address_state);"',
            '        public string UpdateCommand => "UPDATE customer  '
            'SET first_name = @first_name, last_name = @last_name, '
            'shipping_address_street_address = '
            '@shipping_address_street_address, '
            'shipping_address_city = @shipping_address_city, '
            'shipping_address_state = @shipping_address_state, '
            'billing_address_street_address = @billing_address_street_address,'
            ' billing_address_city = @billing_address_city, '
            'billing_address_state = @billing_address_state;"',
            '        public string DeleteCommand => "DELETE FROM customer;"',
            "    }",
            "}",
        ],
    ),
    FileData(
        file_path="output/path/Ecommerce/src/ProductDal/Repos",
        file_name="CustomerRepo.cs",
        file_content=[
            "using ProductDal.Interfaces",
            "using ProductDal.Models",
            "",
            "namespace ProductDal.Repos",
            "{",
            "public class CustomerRepo"
            "(IDbService DbService, ISqlCommand sqlCommand) : ICustomer",
            "    {",
            "        public async Task<Brand?> GetAsync"
            "(CustomerGetParam customerGetParam)",
            "        {",
            "           return await DbService.GetAsync<Customer>"
            "(sqlCommand.GetCommand, customerGetParam);",
            "        }",
            "",
            "         public async Task<IEnumerable<Customer>> ListAsync"
            "(CustomerListParam customer)",
            "        {",
            "           return await dbService.ListAsync<Customer>"
            "(sqlCommand.ListCommand, customer);",
            "        }",
            "",
            "        public async Task<int> CreateAsync(Customer customer)",
            "        {",
            "           return await dbService.ExecuteAsync"
            "(sqlCommand.CreateCommand, customer);",
            "        }",
            "",
            "        public async Task<int> UpdateAsync(Customer customer)",
            "        {",
            "           return await dbService.ExecuteAsync"
            "(sqlCommand.UpdateCommand, customer);",
            "        }",
            "",
            "        public async Task<int> DeleteAsync"
            "(CustomerGetParam customerGetParam)",
            "        {",
            "           return await dbService.ExecuteAsync"
            "(sqlCommand.DeleteCommand, customerGetParam);",
            "        }",
            "    }",
            "}",
        ],
    ),
]


class TestDbServiceGenerator(unittest.TestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        self.svc_dir = DbServiceUtil(
            output_path=OUTPUT_PATH,
            sln_name=ECOMMERCE,
            service_name=PRODUCT_DAL,
            src=SRC
        )

    @parameterized.expand([
        (
            "ecommerce_entities",
            [BRAND_ENTITY, CATEGORY_ENTITY, PRODUCT_ENTITY],
            ECOMMERCE_FILE_DATA,
        ),
        (
            "dotnet_types_entity",
            [DOT_NET_TYPE_ENTITY],
            DOTNET_TYPE_ENTITY_FILE_DATA,
        ),
        (
            "customer_address_entity",
            [ADDRESS_ENTITY, CUSTOMER_ENTITY],
            CUSTOMER_ADDRESS_ENTITY_FILE_DATA
        )
    ])
    def test_gen_service(
        self,
        name: str,
        entities: List[Entity],
        expected_file_data: List[FileData]
    ):
        service_gen = DbServiceGenerator(
            service_name=PRODUCT_DAL,
            svc_dir=self.svc_dir,
            entities=entities,
            pl_type_mapper=CSharpTypeMapper(),
            db_type_mapper=None,
            sql_gen=PgsqlCommandGenerator(entity=None)
        )
        actual_file_data = list(service_gen.gen_service())
        self.assertEqual(expected_file_data, actual_file_data)
