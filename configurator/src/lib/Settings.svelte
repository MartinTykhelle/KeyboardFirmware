<script>
  import { db, newLayout, loadLayout } from "./db";
  import { currentLayoutId, currentLayout } from "./stores";

  let layoutSetting = {
    layoutName: "",
    rows: 5,
    columns: 8,
    layerCount: 1,
  };

  async function createNewLayout() {
    newLayout(layoutSetting).then(async (layoutId) => {
      $currentLayoutId = layoutId;
      $currentLayout = await loadLayout($currentLayoutId);
    });
  }
</script>

<table>
  <tbody>
    <tr>
      <td>Name</td>
      <td>
        <input
          bind:value={layoutSetting.layoutName}
          type="text"
          placeholder="Layout Name"
        />
      </td>
    </tr>
    <tr>
      <td>Rows</td>
      <td><input bind:value={layoutSetting.rows} type="number" /></td>
    </tr>
    <tr>
      <td>Columns</td>
      <td><input bind:value={layoutSetting.columns} type="number" /></td>
    </tr>
    <tr>
      <td>Layers</td>
      <td><input bind:value={layoutSetting.layerCount} type="number" /></td>
    </tr>
    <tr>
      <td colspan="2"><button onclick={createNewLayout}>New Layout</button></td>
    </tr>
  </tbody>
</table>

<style>
  input {
    width: 96%;
  }
  button {
    width: 100%;
  }
</style>
