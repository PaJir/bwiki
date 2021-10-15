$("#pcr-calculator").html('
<div class="level-info">
<div class="input-row">
    <label>角色星级(暂不含6星装备物属性)</label>
    <select id="star-select" onChange="changeStar()">
        <option value="6">6</option>
        <option value="5" selected="selected">5</option>
        <option value="4">4</option>
        <option value="3">3</option>
        <option value="2">2</option>
        <option value="1">1</option>
    </select>
    <label>、角色等级</label>
</div>
<div class="input-row">
    <input type="text" name="level" value="142" id="level-select" style="width: 50px" onChange="changeLevel()" />
    <label>、专武等级(开发中)</label>
    <!--<input type="text" name="level" value="140" id="level-select" style="width:50px" onChange="changeLevel()" />-->
</div>
<div class="input-row">
    <label>角色rank</label>
    <select id="rank-select" onChange="changeRank()">
        <option value="14" selected="selected">14</option>
        <option value="13">13</option>
        <option value="12">12</option>
        <option value="11">11</option>
        <option value="10">10</option>
        <option value="9">9</option>
        <option value="8">8</option>
        <option value="7">7</option>
        <option value="6">6</option>
        <option value="5">5</option>
        <option value="4">4</option>
        <option value="3">3</option>
        <option value="2">2</option>
        <option value="1">1</option>
    </select>
</div>
<div class="input-row">
    <label>左上</label>
    <input type="checkbox" id="equip1" onChange="changeEquip(this.id, this.checked)" />
    <label> 左中</label>
    <input type="checkbox" id="equip3" onChange="changeEquip(this.id, this.checked)" />
    <label> 左下</label>
    <input type="checkbox" id="equip5" onChange="changeEquip(this.id, this.checked)" />
    <label> 右上</label>
    <input type="checkbox" id="equip2" onChange="changeEquip(this.id, this.checked)" />
    <label> 右中</label>
    <input type="checkbox" id="equip4" onChange="changeEquip(this.id, this.checked)" />
    <label> 右下</label>
    <input type="checkbox" id="equip6" onChange="changeEquip(this.id, this.checked)" />
    <label> (默认不强化,开发中)</label>
</div>
<div class="input-row">
    <label>包含同角色羁绊属性(开发中)</label>
    <!--<input type="checkbox" id="love-select" onChange="changeLove()" checked />-->
</div>
</div>
</div>
');
