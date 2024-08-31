export default function RadioGroup({
  group,
  items,
}: {
  group: string;
  items: CheckBoxItem[];
}) {
  return (
    <fieldset>
      <div className="flex flex-row space-x-2 mt-2">
        <legend>{group}</legend>
        {items.map((x) => {
          const id = "rdo_" + x.value.replace(" ", "_");
          return (
            <div key={id} className="flex flex-row space-x-1">
              <input
                type="radio"
                id={id}
                name={group}
                value={x.value}
                defaultChecked={x.isChecked}
                onClick={(e: any) => e.target.form.requestSubmit()}
              />
              <label htmlFor={id}>{x.label}</label>
            </div>
          );
        })}
      </div>
    </fieldset>
  );
}
