from rest_framework.response import Response
from rest_framework import status


def patch_error_handler(func):
    def wrapper(self, request, **kwargs):
        allowed_fields_to_change = ['post_title', 'post_body']
        allowed_fields_to_change_count = len(allowed_fields_to_change)
        error_message = ''
        # i use '>=' instead of '>' here, because full replacement must be PUT request, not patch
        if len(request.data) >= allowed_fields_to_change_count: 
            error_message = 'Too many inputs. Use PUT if you want to change all the fields'
        # because i'm dealing with the request.data, which is a dict, it will remove all the ducplicate fields for me, so i don't
        # have to check for copies in an input
        else:
            for field in request.data.keys():
                if field not in allowed_fields_to_change:
                    error_message = f'* {field} * field is invalid'
                    break
        if not error_message: # i wanna put 'func' call into this 'if' statement instead of using for-else block
            return func(self, request, **kwargs)
        
        return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
    return wrapper