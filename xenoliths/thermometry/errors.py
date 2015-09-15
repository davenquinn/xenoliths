def aggregate_errors(T, combine_bases=[]):
    """Quadratic sum of errors with same tag. Provides contribution to total error."""
    def get_components():
        for var, error in T.error_components().iteritems():
            tag = var.tag
            for base in combine_bases:
                if base in var.tag:
                    tag = base
                    break
            yield tag, errors.get(tag,0) + error**2
    return {t: e**.5 for t,e in get_components()}
