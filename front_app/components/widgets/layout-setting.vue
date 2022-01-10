<template>
  <div>
    <!-- theme setting -->
    <a href="javascript:void(0)">
      <div class="setting-sidebar" id="setting-icon" @click="openlayoutSidebar()">
        <div>
          <i class="fa fa-cog" aria-hidden="true"></i>

        </div>
      </div>
    </a>
    <div id="setting_box" class="setting-box" :class="{ opensetting:layoutsidebar }">
      <a href="javascript:void(0)" class="overlay" @click="closelayoutSidebar()"></a>
      <div class="setting_box_body">
        <div>
          <div class="sidebar-back text-left" @click="closelayoutSidebar()">
            <i class="fa fa-angle-left pr-2" aria-hidden="true"></i> Back
          </div>
        </div>
        <div class="setting-body">
          <div class="setting-title" @click="opensettingcontent('color option')">
            <h4>
              color option
              <span class="according-menu"></span>
            </h4>
          </div>
           <div class="setting-contant"  :class="{ opensubmenu: isActive('color option')}">
                    <ul class="color-box">
                        <li>
                            <input id="colorPicker1" type="color" :value="layout.config.color" name="Background" @change="customizeThemeColor($event)">
                            <span>theme deafult color</span>
                        </li>
                    </ul>
                </div>
        </div>
      </div>
    </div>
    <!-- theme setting -->
    <div class="sidebar-btn dark-light-btn">
      <div class="dark-light">
        <div class="theme-layout-version" @click="customizeLayoutVersion()">Dark</div>
      </div>
    </div>

  </div>
</template>
<script>
import { mapState } from 'vuex'
export default {
  name:"layout_setting",
  data() {
    return {
      layoutsidebar: false,
      activeItem: 'home',
      layoutType: 'ltr',
      modalShow: false,
    }
  },
  computed: {
    ...mapState({
      layout: state => state.layout.layout
    })
  },
  created() {
    this.$store.dispatch('layout/set')
    if (process.client) {
      this.activeColor = localStorage.getItem('color')
    }
  },
  methods: {
    openlayoutSidebar() {
      this.layoutsidebar = true
    },
    closelayoutSidebar() {
      this.layoutsidebar = false
    },
    isActive: function (menuItem) {
      return this.activeItem === menuItem
    },
    opensettingcontent: function (menuItem) {
      if (this.activeItem === menuItem) {
        this.activeItem = ''
      } else {
        this.activeItem = menuItem
      }
    },
    customizeLayoutType(val) {
      this.$store.dispatch('layout/setLayoutType', val)
      this.layoutType = val
    },
    selectedColor: function (menuItem) {
      return this.activeColor === menuItem
    },
    customizeThemeColor(val) {
      console.log(val)
      console.log(event.target.value)
      this.$store.dispatch('layout/setColorScheme', event.target.value)
        document.documentElement.style.setProperty('--theme-deafult', event.target.value);
    },
    customizeLayoutVersion() {
      this.$store.dispatch('layout/setLayoutVersion')
    }
  }
}
</script>
