<script>
  import { db, newLayout, loadLayout } from "./db";
  import { currentLayoutId, currentLayout } from "./stores";
  import AttrPair from "./AttrPair.svelte";

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

<div class="flex-vertical">
  <AttrPair>
    <span slot="label">Name</span>
    <span slot="content">
      <input
        bind:value={layoutSetting.layoutName}
        type="text"
        placeholder="Layout Name"
      />
    </span>
  </AttrPair>
  <AttrPair>
    <span slot="label">Rows</span>
    <span slot="content"
      ><input bind:value={layoutSetting.rows} type="number" /></span
    >
  </AttrPair>
  <AttrPair>
    <span slot="label">Columns</span>
    <span slot="content"
      ><input bind:value={layoutSetting.columns} type="number" /></span
    >
  </AttrPair>
  <AttrPair>
    <span slot="label">Layers</span>
    <span slot="content"
      ><input bind:value={layoutSetting.layerCount} type="number" /></span
    >
  </AttrPair>

  <button onclick={createNewLayout}>New Layout</button>
</div>

<style>
  .flex-vertical {
    display: flex;
    flex-direction: column;
    gap: 4px;
    padding-top: 10px;
  }
  input {
    width: 80%;
  }
</style>
