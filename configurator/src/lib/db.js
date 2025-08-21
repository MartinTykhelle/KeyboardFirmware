import Dexie from "dexie";

export const db = new Dexie("keyboardConfigurator");
db.version(1).stores({
  conversion: "++id, qmk, jsCode",
  keyboard: "++id, keyboardName",
});

/**
 * @param {string} name
 */
export async function newKeyboard(name) {
  return await db.table("keyboard").add({ keyboardName: name });
}

export async function saveKeyboard(keyboardId, keyboard) {
  return await db.table("keyboard").update(keyboardId, keyboard);
}

export async function loadKeyboard(keyboardId) {
  return await db.table("keyboard").where("id").equals(keyboardId).toArray();
}

export async function loadKeyboards() {
  return await db.table("keyboard").toArray();
}
