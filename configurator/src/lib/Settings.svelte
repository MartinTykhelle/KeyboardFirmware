<script>
  import { db, newLayout } from "./db";
  import { currentLayoutId } from "./stores";

  let layoutSetting = {
    layoutName: "",
    rows: 5,
    columns: 8,
  };
  //save currentLayoutId to a store
  function createNewLayout() {
    newLayout(layoutSetting).then((layoutId) => {
      console.log(layoutId);
      $currentLayoutId = layoutId;
    });
  }
</script>

<div class="flex-vertical">
  <input
    bind:value={layoutSetting.layoutName}
    type="text"
    placeholder="Layout Name"
  />
  <input bind:value={layoutSetting.rows} type="number" />
  <input bind:value={layoutSetting.columns} type="number" />
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
