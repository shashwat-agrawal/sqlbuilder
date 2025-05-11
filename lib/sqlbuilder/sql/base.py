import inspect
import re

class Base():
    def __init__(self):
        self._install_component('PRE_VERBOSE')
        self._install_component('POST_VERBOSE')

    def _install_component(self, name):
        setattr(self, f'_{name}', [])
        setattr(self, f'_{name}_BINDS', [])
        return
    
    @classmethod
    def bind_placeholder(cls):
        raise NotImplementedError('base sql class does not define bind placeholder')

    def to_sql_and_binds(self):
        raise NotImplementedError('base sql class does not implement to_sql_and_binds')

    def __get_sql_and_binds(self, *args):
        sql = []
        binds = []

        def placeholder():
            return '__PLACEHOLDER__'

        def get_sql_binds(in_str):
            return re.findall('[?]{1,2}', in_str)

        for arg in args:
            if not isinstance(arg, str) and not isinstance(arg, list):
                raise ValueError('add component encountered an argument which is not of type: [str, list]')

            if isinstance(arg, str):
                sql_binds = get_sql_binds(arg)
                if len(sql_binds) > 0:
                    raise ValueError(f'binds found in string type argument. use list to supply bind values. see: {arg}')
            else:
                if len(arg) == 1:
                    raise ValueError('length should be greated than one for list arg type.')

                if not isinstance(arg[0], str):
                    raise ValueError('first element of list type argument should be string, but got: ' + type(arg[0]).__name__)

                sql_binds = get_sql_binds(arg[0])

                if len(sql_binds) != len(arg) - 1:
                    raise ValueError('number of binds supplied for sql [' + arg[0]  + '] should be [' + str(len(sql_binds)) + '] but got [' + str(len(arg) - 1) + ']')

                for bind_index in range(len(sql_binds)):
                    if sql_binds[bind_index] == '?' and not isinstance(arg[bind_index + 1], str) and not isinstance(arg[bind_index + 1], int):
                        raise ValueError(f'bind mismatch at index {bind_index} for sql arg [{arg[0]}]. Expected string or integer type bind')
                    elif sql_binds[bind_index] == '??' and not (isinstance(arg[bind_index +1], list) or isinstance(arg[bind_index + 1], Base)):
                        raise ValueError(f'bind mismatch at index {bind_index} for sql arg [{arg[0]}]. Expected list or nested sql type bind')

        replace_arg_binds = []
        def replace_arg_sql_and_get_binds(matched_object):
            nonlocal replace_arg_binds

            ret_sql = ''
            if matched_object.group(0) == '?':
                ret_sql = placeholder()
            elif isinstance(replace_arg_binds[0], list):
                ret_sql = ','.join([placeholder() for x in range(len(replace_arg_binds[0]))])
            else:
                ret_sql, ignore_binds = replace_arg_binds[0].to_sql_and_binds()

            replace_arg_binds.pop(0)
            return ret_sql

        for arg in args:
            if isinstance(arg, str):
                sql.append(arg)
            else:
                replace_arg_sql = arg[0]
                replace_arg_binds = arg[1:]
        
                arg_sql = re.sub('[?]{1,2}', replace_arg_sql_and_get_binds, replace_arg_sql)
                arg_sql = re.sub(placeholder(), self.bind_placeholder(), arg_sql)
                sql.append(arg_sql)
                for bind in arg[1:]:
                    if not isinstance(bind, list) and not isinstance(bind, Base):
                        binds.append(bind)
                    elif isinstance(bind, list):
                        binds.extend(bind)
                    else:
                        ignore_sql, bind_binds = bind.to_sql_and_binds()
                        binds.extend(bind_binds)
        return sql, binds
    
    def _add_to_component(self, *args):
        name = inspect.stack()[1].function
        has_component = hasattr(self, f'_{name}') and isinstance(getattr(self, f'_{name}'), list)
        has_component_binds = hasattr(self, f'_{name}_BINDS') and isinstance(getattr(self, f'_{name}_BINDS'), list)
        if not has_component or not has_component_binds:
            raise Exception(f'adding sql/binds to a non existed component {name}')

        sql, binds = self.__get_sql_and_binds(*args)
        component_sql = getattr(self, f'_{name}')
        component_binds = getattr(self, f'_{name}_BINDS')

        setattr(self, f'_{name}', component_sql + sql)
        setattr(self, f'_{name}_BINDS', component_binds + binds)

        return

    def _empty_component(self):
        name = inspect.stack()[1].function
        name = re.sub('^REPLACE_', '', name)
        has_component = hasattr(self, f'_{name}') and isinstance(getattr(self, f'_{name}'), list)
        has_component_binds = hasattr(self, f'_{name}_BINDS') and isinstance(getattr(self, f'_{name}_BINDS'), list)
        if not has_component or not has_component_binds:
            raise Exception(f'emptying a non existed component {name}')

        self._install_component(name)

