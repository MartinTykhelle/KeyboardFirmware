<script>
  import { db, newLayout, loadLayout } from './db';
  import { currentLayoutId, currentLayout } from './stores';

  let layoutSetting = {
    layoutName: '',
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
  <input bind:value={layoutSetting.layoutName} type="text" placeholder="Layout Name" />
  Rows: <input bind:value={layoutSetting.rows} type="number" />
  Columns: <input bind:value={layoutSetting.columns} type="number" />
  Layers: <input bind:value={layoutSetting.layerCount} type="number" />
  <button onclick={createNewLayout}>New Layout</button>
</div>

<style>
  .flex-vertical {
    display: flex;
    flex-direction: column;
    gap: 4px;
    padding-top: 10px;
  }
</style>
