from django.contrib.auth import get_user_model
from rest_framework import serializers

from reward.models import Product, Reward, ProductLike, Funding, FundingOrder

User = get_user_model()


class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward

        fields = (
            'pk',
            'reward_name',
            'reward_option',
            'reward_price',
            'reward_shipping_charge',
            'reward_expecting_departure_date',
            'reward_total_count',
            'reward_sold_count',
            'reward_on_sale',
            'product',
        )


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product

        fields = (
            'pk',
            'product_name',
            'product_type',
            'product_company_name',
            'product_img',
            'product_detail_img',
            'product_interested_count',
            'product_start_time',
            'product_end_time',
            'product_cur_amount',
            'product_total_amount',
            'product_video_url',
            'product_is_funding',

        )


class ProductLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductLike

        fields = (
            'pk',
            'user',
            'product',
            'product_name',
            'product_type',
            'product_company_name',
            'product_img',
            'product_interested_count',
            'product_start_time',
            'product_end_time',
            'product_cur_amount',
            'product_total_amount',
            'product_is_funding',
            'liked_at',
        )


class ProductLikeDeleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductLike

        fields = (
            'id',
            'user',
            'product',
            'liked_at'
        )


class FundingOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundingOrder

        fields = (
            'pk',
            'username',
            'phone_number',
            'address1',
            'address2',
            'comment',
            'requested_at',
            'cancel_at',
        )


class ProductFundingOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product

        fields = (
            'product_name',
            'product_type',
            'product_company_name',
            'product_is_funding',
        )


class RewardFundingSerializer(serializers.ModelSerializer):
    product = ProductFundingOrderSerializer()

    class Meta:
        model = Reward

        fields = (
            'product',
        )


class FundingSerializer(serializers.ModelSerializer):
    reward = RewardFundingSerializer()
    order = FundingOrderSerializer()

    class Meta:
        model = Funding

        fields = (
            'pk',
            'reward',
            'order',
            'reward_amount',
        )


class ProductDetailSerializer(ProductSerializer):
    rewards = RewardSerializer(many=True)

    class Meta(ProductSerializer.Meta):
        fields = (
            'pk',
            'product_name',
            'product_type',
            'product_company_name',
            'product_img',
            'product_detail_img',
            'product_interested_count',
            'product_start_time',
            'product_end_time',
            'product_cur_amount',
            'product_total_amount',
            'product_description',
            'product_video_url',
            'rewards',
        )


class ProductFundingSerializer(RewardSerializer):
    rewards = RewardSerializer(many=True)

    class Meta(ProductSerializer.Meta, RewardSerializer.Meta):
        fields = (
            'pk',
            'product_name',
            'product_end_time',
            'rewards',
        )


class ProductLikeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductLike

        fields = (
            'product',
            'user',
            'product_name',
            'product_interested_count',
        )

    def create(self, validated_data):

        product = Product.objects.get(pk=validated_data['product'].pk)

        user = User.objects.get(pk=validated_data['user'].pk)

        try:
            if ProductLike.objects.filter(user=user, product=product).exists():
                product_like = ProductLike.objects.create(
                    user=user,
                    product=product,
                )

                print('만들어짐')
                product.product_interested_count += 1
                product.save()

                return product_like

        except ValueError:
            print('이미 좋아요 되어있습니다.')


class FundingOrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funding
        fields = (
            'id',
            'user',
            'reward',
            'order',
            'reward_amount',
        )

    def create(self, validated_data):
        reward = Reward.objects.get(pk=validated_data['reward'].pk)

        remain = reward.reward_total_count - reward.reward_sold_count

        request_amount = validated_data['reward_amount']

        try:
            if remain - request_amount > 0:
                order = Funding.objects.create(
                    user=validated_data['user'],
                    reward=validated_data['reward'],
                    order=validated_data['order'],
                    reward_amount=validated_data['reward_amount']
                )

                reward.reward_sold_count += request_amount
                reward.save()

                return order
        except ValueError:
            print('수량이 초과 되었습니다.')

    def update(self, instance, validated_data):
        pass


class FundingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundingOrder
        fields = (
            'pk',
            'username',
            'phone_number',
            'address1',
            'address2',
            'comment'
        )

    def create(self, validated_data):
        funding = FundingOrder.objects.create(
            username=validated_data['username'],
            phone_number=validated_data['phone_number'],
            address1=validated_data['address1'],
            address2=validated_data['address2'],
            comment=validated_data.get('comment')
        )

        print(validated_data)

        return funding


class FundingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundingOrder

        fields = (
            'cancel_at',
        )
