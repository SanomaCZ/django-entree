from entree.common.utils import ENTREE_SAFE


def common(request):
    return {
        'entree': ENTREE_SAFE,
        'entree_user': request.entree_user,
    }
