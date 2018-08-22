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
            'liked_at'
        )


class FundingOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundingOrder

        fields = (
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


class FundingSerializer(serializers.ModelSerializer):
    product = ProductFundingOrderSerializer()
    order = FundingOrderSerializer()

    class Meta:
        model = Funding

        fields = (
            'pk',
            'product',
            'order',
            'reward_amount'
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


class ProductLikeCreateSerializer(ProductSerializer):
    class Meta(ProductSerializer.Meta):
        fields = (
            'pk',
            'product_name',
            'product_interested_count',
        )


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

        print('리워드 판매 카운트 :', reward.reward_sold_count)
        print('리워드 토탈 카운트 :', reward.reward_total_count)

        if reward.reward_total_count > reward.reward_sold_count:
            order = Funding.objects.create(
                user=validated_data['user'],
                reward=validated_data['reward'],
                order=validated_data['order'],
                reward_amount=validated_data['reward_amount']
            )

            reward.reward_sold_count += 1
            reward.save()

        return order

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
