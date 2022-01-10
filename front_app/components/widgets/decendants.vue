<template>
  <div class="box">
    <div class="box-title">
      <h3>{{ $t('dashboard.followers') }}</h3>
    </div>
    <div class="box-content">
      <el-tree
        class="filter-tree"
        :props="props"
        :load="loadNode"
        node-key="id"
        @node-click="ClickNode"
        lazy
        :filter-node-method="filterNode"
        :render-content="renderContent"
        ref="tree">
      </el-tree>
    </div>
  </div>

</template>

<script>

import {mapState, mapGetters} from "vuex"
import {axios} from "@/plugins/axios";
import {Tree} from "element-ui"

export default {
  name: "user_decendants",
  data() {
    return {
      props: {
        label: 'username',
        children: 'children',
        isLeaf: 'leaf',
        followers: 'get_descendants_count',
        user_id: 0
      },
      selectedUser: {}
    }
  },
  middleware: ["authenticated"],
  components: {
    "el-tree": Tree,
    VueQrcode: () => import('vue-qrcode')
  },
  computed: {
    ...mapGetters({
      profile: "authfack/profile_info",
      ME: "authfack/ME",
    }),
  },
  methods: {
    loadNode(node, resolve) {
      let vm = this;
      if (node.level === 0) {
        return resolve([{username: this.ME.username, user_id: this.ME.profile.user, follower: 0}]);
      }
      axios.$post(`auth/profiles/${node.data.user_id}/retrieve_children/`)
        .then((response) => {
          if (response.result) {
            var new_children = response.data.children.map((node) => {
              node.leaf = node.children.length === 0;
              node.role = node.roles[0];
              return node;
            })
            vm.childrenlist = new_children;
            resolve(new_children)
          }
        });
    },
    ClickNode(data, Node, ev) {
      var list = [];
      if (Node.childNodes.length > 0) {
        list = Node.childNodes.map((node) => {
          return node.data;
        })
      } else {
        list.push(Node.data)
      }
      this.childrenlist = list;
    },
    renderContent(h, {node, data, store}) {
      if (data.get_descendants_count) {
        return (
          <span class="custom-tree-node text-warning">
            <span><i class="ti-sharethis-alt mr-2"></i>{data.username}</span>
            <span class="float-right ml-md-3">{data.get_descendants_count}</span>
          </span>);
      }
      return (
        <span class="custom-tree-node text-success">
          <span><i class="ti-user mr-2"></i>{node.label}</span>
          </span>);

    },
    filterNode(value, data) {
      if (!value) return true;
      return data.username.includes(value)
    }
  }
}
</script>
