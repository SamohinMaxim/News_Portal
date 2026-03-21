def create_or_edit(context, request_path):
    if 'create' in request_path:
        title = 'Добавление '
    else:
        title = 'Редактирование '

    if 'news' in request_path:
        title += 'новости'
    else:
        title += 'статьи'

    context['create_or_edit'] = title
    return context




# import random
# from .models import Post
#
# post_types = ['NW', 'AR']
#
# authors_id = [3, 4, 5, 6, 7]
#
# def gen_post():
#     for i in range(4, 50):
#         kwargs = {
#             'author_id': random.choice(authors_id),
#             'post_type': random.choice(post_types),
#             'title': f'Заголовок поста {i}',
#             'text': f'Содержание поста {i}'
#         }
#
#         Post.objects.create(**kwargs)
#     print('Все посты успешно созданы!')


