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
            "}"
        ]
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
            "       return await conn.ExecuteAsync(sqlCommand, param);",
            "        }",
            "",
            "        public async Task<T?> GetAsync<T>"
            "(string sqlCommand, object? param)",
            "        {",
            "       return await conn.QuerySingleOrDefaultAsync<T>"
            "(sqlCommand, param);",
            "        }",
            "",
            "        public async Task<IEnumerable<T>> ListAsync<T>"
            "(string sqlCommand, object? param)",
            "        {",
            "       return await conn.QueryAsync<T>(sqlCommand, param);",
            "        }",
            "    }",
            "}"
        ]
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
            "}"
        ]
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
            "}"
        ]
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
            "}"
        ]
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
            "}"
        ]
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
            "}"
        ]
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
            "}"
        ]
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
            "}"
        ]
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
            "}"
        ]
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
            "}"
        ]
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
            "}"
        ]
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
            "}"
        ]
    )
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
            "       return await conn.ExecuteAsync(sqlCommand, param);",
            "        }",
            "",
            "        public async Task<T?> GetAsync<T>"
            "(string sqlCommand, object? param)",
            "        {",
            "       return await conn.QuerySingleOrDefaultAsync<T>"
            "(sqlCommand, param);",
            "        }",
            "",
            "        public async Task<IEnumerable<T>> ListAsync<T>"
            "(string sqlCommand, object? param)",
            "        {",
            "       return await conn.QueryAsync<T>(sqlCommand, param);",
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
            "       return await conn.ExecuteAsync(sqlCommand, param);",
            "        }",
            "",
            "        public async Task<T?> GetAsync<T>"
            "(string sqlCommand, object? param)",
            "        {",
            "       return await conn.QuerySingleOrDefaultAsync<T>"
            "(sqlCommand, param);",
            "        }",
            "",
            "        public async Task<IEnumerable<T>> ListAsync<T>"
            "(string sqlCommand, object? param)",
            "        {",
            "       return await conn.QueryAsync<T>(sqlCommand, param);",
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
            "        public string shipping_address_city "
            "{ get; set; } = default!;",
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
            db_type_mapper=None
        )
        actual_file_data = list(service_gen.gen_service())
        self.assertEqual(expected_file_data, actual_file_data)
