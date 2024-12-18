import { useRef } from "react";

export default function CheckboxGroup({
  items,
  group,
}: {
  items: CheckBoxItem[];
  group: string;
}) {
  const ref: any = useRef([]);

  const uncheckAll = (e: any) => {
    e.preventDefault();
    for (let i = 0; i < ref.current.length; i++) {
      ref.current[i].checked = false;
    }
    e.target.form.requestSubmit();
  };

  const checkAll = (e: any) => {
    e.preventDefault();
    for (let i = 0; i < ref.current.length; i++) {
      ref.current[i].checked = true;
    }
    e.target.form.requestSubmit();
  };

  return (
    <div className="form-group form-checkbox flex flex-col space-y-1 lg:flex-row lg:space-x-1 lg:items-center">
      <legend>{group}</legend>
      <div className="lg:hidden flex flex-row space-x-2">
        <button onClick={checkAll} className="form-button">
          (select all)
        </button>
        <button onClick={uncheckAll} className="form-button">
          (unselect all)
        </button>
      </div>
      {items.map((x, idx) => {
        const id = "chk_" + x.value.replace(" ", "_");
        return (
          <div key={id} className="flex flex-row space-x-1">
            <input
              type="checkbox"
              ref={(element) => {
                ref.current[idx] = element;
              }}
              name={group}
              id={id}
              value={x.value}
              defaultChecked={x.isChecked}
              onClick={(e: any) => e.target.form.requestSubmit()}
            />
            <label htmlFor={id}>{x.label}</label>
          </div>
        );
      })}

      {/* Buttons only for horiztonal layout */}
      <div className="hidden lg:flex lg:flex-row lg:space-x-2">
        <button onClick={checkAll} className="form-button">
          (select all)
        </button>
        <button onClick={uncheckAll} className="form-button">
          (unselect all)
        </button>
      </div>
    </div>
  );
}
