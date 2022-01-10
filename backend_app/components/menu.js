export const Menu = [
  {
    id: 1,
    label: "menuitems.navigation.text",
    isTitle: true,
    roles: ["superadmin"],
  },
  {
    id: 2,
    label: "menuitems.dashboard.text",
    icon: "ri-dashboard-line",
    badge: {
      variant: "success",
      text: "menuitems.dashboard.badge"
    },
    isMenuCollapsed: true,
    subItems: [
      {
        id: 3,
        label: 'menuitems.dashboard.list.sales',
        link: '/'
      },
    ],
    roles: ["superadmin"],
  },
  {
    id: 3,
    label: "menuitems.ecommerce.text",
    isTitle: true,
    roles: ["superadmin"],
  },
  {
    id: 4,
    label: "menuitems.ecommerce.point_management.title",
    icon: "ri-coin-fill",
    isMenuCollapsed: false,
    roles: ["superadmin"],
    badge: {
      variant: "danger",
      text: "menuitems.ecommerce.badge"
    },
    subItems: [
      {
        id: 40,
        label: "menuitems.ecommerce.point_management.pointbanks.title",
        link: "/superadmin/pointbanks",
        icon: "ri-coin-fill text-danger"
      },
      {
        id: 41,
        label: "menuitems.ecommerce.point_management.point_history.title",
        link: "/superadmin/points",
        icon: "ri-coin-fill text-warning"
      },
    ]
  },
  {
    id: 5,
    label: "menuitems.product.text",
    icon: "ri-dashboard-fill",
    badge: {
      variant: "danger",
      text: "menuitems.ecommerce.badge"
    },
    isMenuCollapsed: false,
    roles: ["superadmin"],
    subItems: [
      {
        id: 51,
        label: "menuitems.product.regular",
        link: "/superadmin/products"
      },
      {
        id: 52,
        label: "menuitems.product.inventory",
        link: "/superadmin/variations"
      },
      {
        id: 53,
        label: "menuitems.product.all_comments",
        link: "/superadmin/products/comments/all"
      },
      {
        id: 54,
        label: "menuitems.product.pingo",
        link: "/superadmin/pingoproducts"
      },
    ]
  },
  {
    id: 8,
    label: "menuitems.ecommerce.text",
    icon: "fe-shopping-cart",
    badge: {
      variant: "danger",
      text: "menuitems.ecommerce.badge"
    },
    isMenuCollapsed: false,
    roles: ["superadmin"],
    subItems: [
      {
        id: 80,
        label: "menuitems.ecommerce.orders.text",
        link: "/superadmin/orders"
      },
      {
        id: 81,
        label: "menuitems.ecommerce.supplier_orders.text",
        link: "/superadmin/orders/supplier_orderlist"
      },
      {
        id: 82,
        label: "menuitems.ecommerce.pingo_orders.text",
        link: "/superadmin/pingo_orders"
      },
    ]
  },
  {
    id: 9,
    label: "menuitems.organizations.text",
    icon: "fe-git-merge",
    badge: {
      variant: "danger",
      text: "menuitems.ecommerce.badge"
    },
    isMenuCollapsed: false,
    roles: ["superadmin"],
    subItems: [
      {
        id: 91,
        label: "menuitems.organizations.supplier.text",
        link: "/superadmin/suppliers"
      },
      {
        id: 92,
        label: "menuitems.organizations.client.text",
        link: "/superadmin/clients"
      },
      {
        id: 93,
        label: "menuitems.organizations.user.text",
        link: "/superadmin/users"
      },
      // {
      //   id: 94,
      //   label: "menuitems.organizations.customer.text",
      //   link: "/superadmin/customers"
      // },
    ]
  },
  {
    id: 7,
    label: "menuitems.system.text",
    icon: "fe-settings",
    badge: {
      variant: "danger",
      text: "menuitems.ecommerce.badge"
    },
    isMenuCollapsed: false,
    roles: ["superadmin"],
    subItems: [
      {
        id: 71,
        label: "menuitems.system.text",
        link: "/superadmin/system"
      },
      {
        id: 73,
        label: "menuitems.ecommerce.list.shop_faqs",
        link: "/superadmin/faqs"
      },
    ]
  },


  // menuitems for client_admin
  {
    id: 201,
    label: "menuitems.navigation.text",
    isTitle: true,
    roles: ["client"],
  },

  {
    id: 202,
    label: "menuitems.dashboard.text",
    icon: "ri-dashboard-line",
    badge: {
      variant: "success",
      text: "menuitems.dashboard.badge"
    },
    isMenuCollapsed: true,
    subItems: [
      {
        id: 2021,
        label: 'menuitems.dashboard.list.followers',
        link: '/client/followers',
        icon: "ri-team-line text-success"
      },
      {
        id: 2022,
        label: 'menuitems.ecommerce.points.text',
        link: '/client/points',
        icon: "ri-coin-fill text-warning"
      },
    ],
    roles: ["client"],
  },

    // menuitems for supplier
  {
    id: 301,
    label: "menuitems.navigation.text",
    isTitle: true,
    roles: ["supplier"],
  },

  {
    id: 302,
    label: "menuitems.dashboard.text",
    icon: "ri-dashboard-line",
    badge: {
      variant: "success",
      text: "menuitems.dashboard.badge"
    },
    isMenuCollapsed: true,
    subItems: [
      {
        id: 3021,
        label: 'menuitems.dashboard.list.orders',
        link: '/supplier/orders',
        icon: " ri-list-unordered text-success"
      },
      {
        id: 3021,
        label: 'menuitems.ecommerce.list.products',
        link: '/supplier/products',
        icon: " ri-price-tag-3-fill text-success"
      },
    ],
    roles: ["supplier"],
  },
];

export default Menu;
