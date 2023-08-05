import re
import theano
import numpy

# https://gist.github.com/danielrenshaw/4b8b2d723a2d7319192f
class Debug(theano.gof.Op):
    view_map = {0: [0]}

    __props__ = ('name', 'debug_level', 'check_not_all_nan', 'check_not_any_nan', 'check_not_all_inf',
                 'check_not_any_inf', 'raise_on_failed_nan_check', 'raise_on_failed_inf_check')

    def _check(self, check_not_all, check_not_any, masker, value, prefix):
        if self.debug_level > 0 or check_not_all or check_not_any:
            mask = masker(value)

            if mask.all():
                info = 'all'
                failed_check = check_not_all
            elif mask.any():
                info = 'some'
                failed_check = check_not_any
            else:
                info = 'none'
                failed_check = False

            return '<%s: %s>' % (prefix, info), failed_check

    def _test_exception(self, exception, return_exception):
        if exception is None:
            return None

        if return_exception:
            return exception

        raise exception

    def _action_check(self, check_failed, name, check_type, node, force_print, return_exception):
        exception = None

        if check_failed or force_print:
            if node is not None:
                print ('*** %s pp:' % name)
                print (theano.printing.pp(node))
                print ('*** %s debugprint (all):' % name)
                import pdb;pdb.set_trace()
                print (theano.printing.debugprint(node, ids='id', print_type=True, print_storage=True))
                print ('*** %s debugprint (limited):' % name)
                print (theano.printing.debugprint(node, ids='id', print_type=True, print_storage=True))

            exception = Exception('Failed %s %s check' % (name, check_type))

        return self._test_exception(exception, return_exception)

    def _print_value(self, value, name, node=None, enable_all_checks=False, disable_all_checks=False, force_print=False,
                     return_exception=False):
        exception = None

        if force_print or self.debug_level > 0:
            check_not_all_nan = enable_all_checks or self.check_not_all_nan
            check_not_any_nan = enable_all_checks or self.check_not_any_nan
            check_not_all_inf = enable_all_checks or self.check_not_all_inf
            check_not_any_inf = enable_all_checks or self.check_not_any_inf
            nan_info, nan_check_failed = self._check(check_not_all_nan, check_not_any_nan, numpy.isnan, value, 'nan')
            inf_info, inf_check_failed = self._check(check_not_all_inf, check_not_any_inf, numpy.isinf, value, 'inf')

            if disable_all_checks:
                nan_check_failed = False
                inf_check_failed = False

            if force_print or nan_check_failed or inf_check_failed or self.debug_level > 1:
                name = '%s.%s' % (self.name, name)

                if isinstance(value, numpy.ndarray):
                    type_info = '<type: %s %s>' % (value.dtype, value.shape)
                else:
                    type_info = type(value)

                print ('%s %s %s %s' % (name, type_info, nan_info, inf_info),)
                print (re.sub('\\s+', ' ', repr(value)) if self.debug_level > 1 else '')

                exception = self._action_check(self.raise_on_failed_nan_check and nan_check_failed, name, 'nan', node,
                                               force_print, return_exception) if exception is None else exception
                exception = self._action_check(self.raise_on_failed_inf_check and inf_check_failed, name, 'inf', node,
                                               force_print, return_exception) if exception is None else exception

        return self._test_exception(exception, return_exception)

    def _print_test_value(self, node, name, enable_all_checks=False, disable_all_checks=False, force_print=False,
                          return_exception=False):
        exception = None

        if (force_print or self.debug_level > 0) and \
                        node is not None and hasattr(node, 'tag') and \
                        node.tag is not None and hasattr(node.tag, 'test_value'):
            exception = self._print_value(node.tag.test_value, name + '.test_value', node=node,
                                          enable_all_checks=enable_all_checks, disable_all_checks=disable_all_checks,
                                          force_print=force_print, return_exception=return_exception)

        return self._test_exception(exception, return_exception)

    def _print_test_values(self, nodes, parent_name, name, other_nodes=None, enable_all_checks=False,
                           disable_all_checks=False):
        exception = None

        for node_index, node in enumerate(nodes):
            exception = self._print_test_value(node, '%s.%s.%s' % (parent_name, name, node_index),
                                               enable_all_checks=enable_all_checks,
                                               disable_all_checks=disable_all_checks,
                                               return_exception=True) if exception is None else exception

        if exception is not None and other_nodes is not None:
            if not isinstance(other_nodes, (tuple, list)):
                other_nodes = [other_nodes]

            for other_node_index, other_node in enumerate(other_nodes):
                self._print_test_value(other_node, '%s.%s.%s' % (parent_name, name, other_node_index), force_print=True,
                                       return_exception=True)

        return self._test_exception(exception, False)

    def __init__(self, name, debug_level, check_not_all_nan=True, check_not_any_nan=False, check_not_all_inf=True,
                 check_not_any_inf=False, raise_on_failed_nan_check=False, raise_on_failed_inf_check=False):
        self.name = name
        self.debug_level = debug_level
        self.check_not_all_nan = check_not_all_nan
        self.check_not_any_nan = check_not_any_nan
        self.check_not_all_inf = check_not_all_inf
        self.check_not_any_inf = check_not_any_inf
        self.raise_on_failed_nan_check = raise_on_failed_nan_check
        self.raise_on_failed_inf_check = raise_on_failed_inf_check
        super(Debug, self).__init__()

    def make_node(self, input_node):
        assert not isinstance(input_node, (tuple, list))
        # No need to print test value here because, if test values are enabled, "perform" will be called with the test
        # value as input. If this comment is wrong, could use the following line here, but may produce duplicate output.
        # self._print_test_value(input_node, 'make_node.input_node')
        return theano.gof.Apply(op=self, inputs=[input_node], outputs=[input_node.type.make_variable()])

    def perform(self, node, input_values, output_storage):
        input_value = input_values[0]
        output_storage[0][0] = input_value
        self._print_value(input_value, 'perform.input_value', node=node.inputs[0])

    def grad(self, input_nodes, output_gradients):
        # We cannot be sure that input or output gradients will avoid nans and infs, even if the expressions being
        # debugging by this instance cannot themselves generate nans or infs, hence the use of disable_all_checks.
        self._print_test_values(input_nodes, 'grad', 'input_node', other_nodes=output_gradients,
                                disable_all_checks=True)
        self._print_test_values(output_gradients, 'grad', 'output_gradient', other_nodes=input_nodes,
                                disable_all_checks=True)
        return output_gradients

    def R_op(self, input_nodes, eval_points):
        self._print_test_values(input_nodes, 'R_op', 'input_node', other_nodes=eval_points)
        self._print_test_values(eval_points, 'R_op', 'eval_point', other_nodes=input_nodes)
        return eval_points

    def __setstate__(self, dct):
        self.__dict__.update(dct)

    def c_code_cache_version(self):
        return 1,


def debug(node, name, debug_level, check_not_all_nan=True, check_not_any_nan=False, check_not_all_inf=True,
          check_not_any_inf=False, raise_on_failed_nan_check=True, raise_on_failed_inf_check=True):
    node.name = name
    result = Debug(name, debug_level, check_not_all_nan, check_not_any_nan, check_not_all_inf, check_not_any_inf,
                   raise_on_failed_nan_check, raise_on_failed_inf_check)(node)
    result.name = name
    return result


def dbg(arg, name):
    return debug(arg, name, 1, raise_on_failed_nan_check=True, check_not_all_nan=True)
