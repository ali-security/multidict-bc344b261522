import gc

import objgraph  # type: ignore[import-untyped]

from multidict import CIMultiDict, MultiDict


class SubtractionOperandValue:
    pass


class ReflectedUnionOperandValue:
    pass


def _run_isolated_case() -> None:
    # Non-empty operands exercise the loop parsing the operand's items.
    for md_cls in (MultiDict, CIMultiDict):
        md = md_cls([("key", "value")])
        for i in range(100):
            sub_operand = [(f"k{i}", SubtractionOperandValue())]
            sub_result = md.items() - sub_operand
            union_operand = [(f"k{i}", ReflectedUnionOperandValue())]
            union_result = union_operand | md.items()
            del sub_operand, sub_result, union_operand, union_result

    gc.collect()
    leaked_subtraction_operand = len(objgraph.by_type("SubtractionOperandValue"))
    leaked_reflected_union_operand = len(objgraph.by_type("ReflectedUnionOperandValue"))
    assert leaked_subtraction_operand == 0, (
        f"{leaked_subtraction_operand} subtraction operand values not collected by GC"
    )
    assert leaked_reflected_union_operand == 0, (
        f"{leaked_reflected_union_operand} reflected union operand values "
        "not collected by GC"
    )


if __name__ == "__main__":
    _run_isolated_case()
