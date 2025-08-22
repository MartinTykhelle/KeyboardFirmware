import Dexie from "dexie";

export const db = new Dexie("keyboardConfigurator");
db.version(1).stores({
  conversion: "++id, qmk, jsCode",
  layout: "++layoutId, layoutName",
});

export async function newLayout(layout) {
  layout.layoutId = undefined;
  layout.keys = [];
  for (let rowId = 0; rowId < layout.rows; rowId++) {
    let row = [];
    for (let columnId = 0; columnId < layout.columns; columnId++) {
      row.push({ width: 1, qmk: "KC_NO" });
    }
    layout.keys.push(row);
  }
  return await db.table("layout").add(layout);
}

export async function saveLayout(layoutId, layout) {
  return await db.table("layout").update(layoutId, layout);
}

export async function loadLayout(layoutId) {
  return await db.table("layout").where("layoutId").equals(layoutId).toArray();
}

export async function loadLayouts() {
  return await db.table("layout").toArray();
}
