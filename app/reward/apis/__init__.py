import datetime

from django.contrib.auth import get_user_model
from rest_framework import generics, mixins, filters
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Product, Reward, ProductLike, Funding, FundingOrder
from ..serializer import ProductSerializer, RewardSerializer, ProductDetailSerializer, ProductFundingSerializer, \
    ProductLikeSerializer, FundingSerializer, ProductLikeCreateSerializer, FundingCreateSerializer, \
    FundingOrderCreateSerializer, FundingUpdateSerializer, ProductLikeDeleteSerializer
from utils.paginations import ProductListPagination

User = get_user_model()


# DB 에서 Product 모든 정보를 요청한다.
class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductListPagination


# Product 의 검색기능.
class ProductCategoryList(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductListPagination

    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('product_interested_count', 'product_cur_amount', 'product_start_time', 'product_end_time')

    def get_queryset(self):
        category = self.request.query_params.get('category', '')
        product_name = self.request.query_params.get('product_name', '')
        is_funding = self.request.query_params.get('is_funding', 'A')

        return Product.objects.filter(product_type__contains=category, product_name__contains=product_name,
                                      product_is_funding__contains=is_funding)


# 좋아하는 Product 리스트를 요청한다.
class ProductLikeList(generics.ListAPIView):
    queryset = ProductLike.objects.all()
    serializer_class = ProductLikeCreateSerializer


# 펀딩한 리워드 정보를 요청한다. (장바구니)
class FundingList(generics.ListAPIView):
    queryset = Funding.objects.all()
    serializer_class = FundingSerializer


# 펀딩 페이지에서 불필요한 리워드 정보를 배제하고 펀딩에 필요한 리워드 정보 요청한다.
class ProductFundingList(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductFundingSerializer


# 리워드 정보를 요청한다.
class RewardList(generics.ListAPIView):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer


# Product 의 Detail 페이지에 관한 정보를 요청한다.
# object 한개를 가져 올때는 generics.RetrieveAPIView 를 사용, CRUD 가능
class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


# 작명 (Api view 를 뒤에 추가 )
class FundingCreate(generics.ListCreateAPIView):
    queryset = FundingOrder.objects.all()
    serializer_class = FundingCreateSerializer

    def patch(self, request, *args, **kwargs):
        funding_pk = self.request.data.get('pk')

        user = User.objects.get(username=request.user)

        funding = Funding.objects.filter(pk=funding_pk, user=user)

        print(type(funding))

        funding.cancel_at = datetime.datetime.now()

        funding.save()

        serializer = self.get_serializer_class()(funding)

        return Response(serializer.data)


class FundingOrderCreate(generics.ListCreateAPIView):
    queryset = Funding.objects.all()
    serializer_class = FundingOrderCreateSerializer


class ProductLikeDelete(generics.DestroyAPIView):
    queryset = ProductLike.objects.all()
    serializer_class = ProductLikeDeleteSerializer

    def delete(self, request, *args, **kwargs):
        # print(self.kwargs['pk'])

        product_like = ProductLike.objects.get(pk=self.kwargs['pk'])

        # print('지우기전:', product_like.product.product_interested_count)

        product_like.product.product_interested_count -= 1
        product_like.product.save()

        # print('지운후:', Product.objects.get(pk=product_like.product.pk).product_interested_count)

        return self.destroy(request, *args, **kwargs)


class ProductLikeCreate(generics.CreateAPIView, generics.ListAPIView):
    queryset = ProductLike.objects.all()

    serializer_class = ProductLikeSerializer

    def post(self, request, *args, **kwargs):
        product = Product.objects.get(pk=self.request.data['product'])

        product.product_interested_count += 1

        product.save()

        print(f'{product.pk}를 좋아요 했습니다.')

        return self.create(request, *args, **kwargs)


class FundingUpdate(generics.UpdateAPIView):
    queryset = FundingOrder.objects.all()
    serializer_class = FundingUpdateSerializer

    def patch(self, request, *args, **kwargs):
        # order 의 Pk 로 order 인스턴스를 얻는다.

        return self.partial_update(request, *args, **kwargs)

    # def get_serializer_class(self):
    #     serializer_class = self.serializer_class
    #
    #     if self.request.method == 'PATCH':
    #         serializer_class = ProductLikeCreateSerializer
    #
    #         return serializer_class
    #
    #     return serializer_class

    # def patch(self, request, *args, **kwargs):
    #     product_pk = self.request.data.get('pk')
    #
    #     user = User.objects.get(username=request.user)
    #
    #     product = Product.objects.get(pk=product_pk)
    #
    #     # 이미 좋아요를 한기록이 있으면 좋아요 삭제 + DB 에서 좋아요 갯수감소
    #     if ProductLike.objects.filter(user=user).exists():
    #
    #         product.product_interested_count -= 1
    #
    #         ProductLike.objects.filter(user=user).delete()
    #
    #         product.save()
    #
    #     # 좋아요 기록이 없으면 좋아요 만들고 DB 에서 좋아요 갯수 증가
    #     else:
    #         ProductLike.objects.create(
    #             user=user,
    #             product=product,
    #         )
    #
    #         product.product_interested_count += 1
    #
    #         product.save()
    #
    #     serializer = self.get_serializer_class()(product)
    #
    #     return Response(serializer.data)
