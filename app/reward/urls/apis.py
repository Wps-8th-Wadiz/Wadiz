from django.urls import path

from .. import apis

urlpatterns = [
    path('', apis.ProductList.as_view()),
    path('search/', apis.ProductCategoryList.as_view()),
    path('<int:pk>/', apis.ProductDetail.as_view()),
    path('<int:pk>/funding/', apis.ProductFundingList.as_view()),
    path('product_like/', apis.ProductLikeCreate.as_view()),
    path('product_like/<int:pk>/', apis.ProductLikeDelete.as_view()),

    path('like_list/', apis.ProductLikeList.as_view()),

    path('funding_create/', apis.FundingCreate.as_view()),

    path('funding_order/', apis.FundingOrderCreate.as_view()),
    path('funding_list/', apis.FundingList.as_view()),
]
