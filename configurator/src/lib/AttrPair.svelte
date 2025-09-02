<div>
  <span class="label"><slot name="label"></slot></span>
  <span class="content"><slot name="content"></slot></span>
</div>

<style>
  div {
    display: flex;
    flex-direction: row;
  }
  span {
    overflow: hidden;
  }
  .label {
    width: 30%;
  }
  .content {
    width: 70%;
  }
</style>
