import random
from .models import UserProfile


def generate_promocode_for_profile(profile):
    """generetes random codes like 'aaa-BBB-999'
       with pairs, delimited by delimiter """
    if profile.promocode_generated:
        return profile.promocode_generated
    pairs = 4
    digits = 6
    delimiter = '-'
    chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

    codes = []
    for n in range(pairs):
        pair = ''
        for d in range(digits):
            pair += random.choice(chars)
        codes.append(pair)
    code = delimiter.join(codes)

    return code


def registration_by_code(user, promo_code):
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = None
    if not user_profile:
        user_profile = UserProfile.objects.create(user=user)

    user_profile.promocode_used = promo_code
    try:
        code_owner = UserProfile.objects.get(promocode_generated=promo_code)
    except UserProfile.DoesNotExist:
        code_owner = None
    if code_owner:
        prize = code_owner.referred.count() + 1
        user_profile.referrer = code_owner
        user_profile.save()

        distribute_points(code_owner, prize)


def distribute_points(profile, prize):
    if prize <= 0:
        return
    if not profile.referrer:
        profile.points += prize
        profile.save()
    else:
        profile.points += 1
        profile.save()
        prize -= 1
        distribute_points(profile.referrer, prize)

