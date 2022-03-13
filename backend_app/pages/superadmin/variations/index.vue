<script>
import Swal from "sweetalert2";
import {
    APIServices
} from "@/helpers/APIs";
import {
    swalService
} from "~/helpers/swal.service";

export default {
    name: "EditProductVariationTable",
    components: {
        // Switches: () => import('vue-switches'),
        "el-upload": () => import("element-ui/lib/upload"),
        "el-table": () => import("element-ui/lib/table"),
        "el-table-column": () => import("element-ui/lib/table-column"),
        VariationModal: () => import("./components/VariationModal"),
    },
    data() {
        return {
            isLoading: false,
            title: "商品在庫",
            items: [{
                    text: "PINGO"
                },
                {
                    text: "eCommerce"
                },
                {
                    text: "商品在庫",
                    active: true
                },
            ],
            showVariationModal: false,
            modeAdd: false,
            search_keyword: "",
            search_sku: "",
            variations: [],
            variations_meta: {
                links: {},
                page: 1,
                page_size: 10,
                total: 0,
            },
            edit_variation: {
                price: 0,
                purchase_price: 0,
                name: "",
                description: "",
                variation_type: "REGULAR",
                inventory: 0,
                sort_by: 0,
                point_rule: {
                    is_valid: false,
                    type: "amount",
                    policies: {
                        client_superadmin: 0,
                        client_admin: 0,
                        level_2: 0,
                        level_1: 0,
                        user_self: 0,
                    },
                    special_promotion: {
                        is_valid: false,
                        bonus: 0,
                    },
                },
            },
        };
    },
    head() {
        return {
            title: `${this.title} | PINGO`,
            script: [{
                src: "https://unpkg.com/element-ui/lib/index.js"
            }],
            link: [{
                rel: "stylesheet",
                href: "https://unpkg.com/element-ui/lib/theme-chalk/index.css",
            }, ],
        };
    },
    computed: {
        csrftoken() {
            return this.$auth.strategy.token.get();
        },
        list_url() {
            return `store/public/variations/?page=${this.variations_meta.page}&page_size=${this.variations_meta.page_size}&sorted_by=inventory,item`;
        },
    },
    mounted() {
        this.load_list();
    },
    methods: {
        tablePageChange(page) {
            this.variations_meta.page = page;
            this.load_list();
        },
        search_variations(byMode) {
            if (this.search_key !== "") {
                const self = this;
                let searchUrl = "";
                if (byMode === "sku") {
                    searchUrl = `/store/public/filter_variations/by_sku/?query=${this.search_sku}`;
                } else {
                    searchUrl = `store/public/filter_variations/by_name_description/?query=${this.search_keyword}`;
                }

                this.isLoading = true;

                APIServices.get(searchUrl)
                    .then(APIServices.handleResponse)
                    .then((response) => {
                        self.variations = response;
                        self.variations_meta.page_size = response.length;
                        self.variations_meta.page = 1;
                        self.variations_meta.total = response.length;
                    });

                this.isLoading = false;
            }
        },
        load_list() {
            const self = this;

            this.$nuxt.$loading.start();
            APIServices.get(this.list_url)
                .then(APIServices.handleResponse)
                .then((response) => {
                    // eslint-disable-next-line no-console
                    console.log(response);
                    self.variations = response.results;
                    self.variations_meta = response.meta;
                });

            this.$nuxt.$loading.finish();
        },
        async InventoryOpt(variation, opt) {
            const vm = this;
            const _tilte = opt === "plus" ? "在庫追加理由" : "在庫削除理由";
            const steps = ["1", "2"]
            const steps_data = [{
                    confirmText: "Forward",
                    cancelText: "Back",
                    title: _tilte,
                    inputType: "text",
                },
                {
                    confirmText: "Submit",
                    cancelText: "Back",
                    title: "変更数量",
                    inputType: "number",
                },
            ];
            const swalQueueStep = Swal.mixin({
                progressSteps: steps,
                inputAttributes: {
                    required: true,
                },
                reverseButtons: true,
                validationMessage: "This field is required",
            });

            const values = [];
            let currentStep;

            for (currentStep = 0; currentStep < steps.length;) {
                const result = await swalQueueStep.fire({
                    confirmButtonText: steps_data[currentStep].confirmText,
                    cancelButtonText: steps_data[currentStep].cancelText,
                    input: steps_data[currentStep].inputType,
                    title: steps_data[currentStep].title,
                    inputValue: values[currentStep],
                    showCancelButton: currentStep > 0,
                    currentProgressStep: currentStep,
                });

                if (result.value) {
                    values[currentStep] = result.value;
                    currentStep++;
                } else if (result.dismiss === Swal.DismissReason.cancel) {
                    currentStep--;
                } else {
                    break;
                }
            }

            if (currentStep === steps.length) {
                const data = {
                    variation: variation.id,
                    type: opt === 'plus' ? 'BS' : 'RS',
                    in_out: opt === 'plus' ? 1 : -1,
                    quantity: values[1],
                    info: values[0]
                }
                Swal.fire({
                    title: "実行しますか",
                    showCancelButton: true,
                    confirmButtonText: '確定',
                    showLoaderOnConfirm: true,
                    preConfirm: (stock) => {
                        return APIServices.post('store/public/inventory/', data)
                            .then(APIServices.handleResponse)
                            .then((response) => {
                                return response
                            })
                            .catch((error) => {
                                Swal.showValidationMessage(`Request failed: ${error}`)
                            })
                    },
                    allowOutsideClick: () => !Swal.isLoading()
                }).then((result) => {
                    if (result.isConfirmed) {
                        APIServices.get(`store/public/variations/${result.value.variation}/`)
                            .then(APIServices.handleResponse)
                            .then((response) => {
                                const index = vm.variations.findIndex(
                                    variation => variation.id === result.value.variation
                                )
                                if (index > -1) {
                                    vm.variations[index].inventory = response.inventory
                                }
                                swalService.showToast('success', '在庫は更新されました！')
                            })
                    }
                })
            }

        },
        switchAddVariationMode() {
            this.modeAdd = true;
            this.showVariationModal = true;
        },

        editVariation(variation) {
            this.edit_variation = variation;
            this.modeAdd = false;
            this.showVariationModal = true;
        },

        getUploadVariationimageURL(id) {
            return `https://www.pingo.jp/daphne/api/store/public/variations/${id}/update_image/`;
        },
        beforeAvatarUpload(file) {
            const isJPG = file.type === "image/jpeg";
            const isLt2M = file.size / 1024 / 1024 < 2;
            // return isLt2M;
            if (!isLt2M || !isJPG) {
                swalService.showModal(
                    "Invalid picture",
                    "Should be JPEG and below 2M",
                    "warning"
                );
                return false;
            }
            return isJPG && isLt2M;
            // return isJPG && isLt2M;
        },
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        handleVariationImageSuccess(res, file) {
            if (res.result) {
                this.ReplaceVariation(res.data);
            }
        },

        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        VariationOperate({
            modeAdd,
            _variation
        }) {
            const vm = this;
            this.ReplaceVariation(_variation);
            vm.showVariationModal = false;
        },
        ReplaceVariation(_variation) {
            const vm = this;
            const index = vm.variations.findIndex(
                (variation) => variation.id === _variation.id
            );
            if (index > -1) {
                vm.variations.splice(index, 1, _variation);
                swalService.showModal("Success", "更新されました!", "success");
            }
        },
    },
};
</script>
<template>
<div>
    <PageHeader :title="title" :items="items" />
    <div class="card">
        <div class="card-body">
            <div class="row mb-2">
                <div class="col-sm-6">
                    <div class="form-group row mb-0">
                        <div class="col-sm-12">
                            <div class="input-group">
                                <input v-model="search_sku" type="text" class="form-control" placeholder="sku" aria-describedby="basic-addon2" />
                                <div class="input-group-append">
                                    <button class="btn btn-success waves-effect waves-light" type="button" @click="search_variations('sku')">
                                        Search SKU
                                        <font-awesome-icon v-if="isLoading" :icon="['fa', 'spinner']" spin />
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-sm-6">
                    <div class="form-group row mb-0">
                        <div class="col-sm-12">
                            <div class="input-group">
                                <input v-model="search_keyword" type="text" class="form-control" placeholder="keyword" aria-describedby="basic-addon2" />
                                <div class="input-group-append">
                                    <button class="btn btn-dark waves-effect waves-light" type="button" @click="search_variations('keywords')">
                                        Search Keywords
                                        <font-awesome-icon v-if="isLoading" :icon="['fa', 'spinner']" spin />
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- end col-->
            </div>
        </div>
    </div>
    <div class="card">
        <div class="card-body">
            <div class="row">
                <div class="table-responsive">
                    <div v-if="variations_meta.total > 0" class="row my-2">
                        <div class="col">
                            <div class="dataTables_paginate paging_simple_numbers float-right">
                                <ul class="pagination pagination-rounded">
                                    <b-pagination v-model="variations_meta.page" pills aria-controls="pingoproduct_table" :total-rows="variations_meta.total" :per-page="variations_meta.page_size" @change="tablePageChange" />
                                </ul>
                            </div>
                        </div>
                    </div>
                    <el-table :data="variations" style="width: 100%" :header-cell-style="{ textAlign: 'center' }">
                        <el-table-column width="250" sortable prop="id">
                            <template slot-scope="scope">
                                <font-awesome-icon :icon="['fa', 'award']" :class="{
                                  'text-success': scope.row.is_valid,
                                  'text-danger': !scope.row.is_valid,
                                }" />
                                <el-upload class="avatar-uploader" :action="getUploadVariationimageURL(scope.row.id)" :show-file-list="false" :headers="{ Authorization: csrftoken }" :on-success="handleVariationImageSuccess" :name="'image'" :before-upload="beforeAvatarUpload">
                                    <img v-if="scope.row.thumbimage_url" :src="scope.row.thumbimage_url" style="max-width: 160px" class="avatar" />
                                    <i v-else class="el-icon-plus avatar-uploader-icon" />
                                </el-upload>
                            </template>
                        </el-table-column>
                        <el-table-column width="250" label="商品名" sortable prop="id">
                            <template slot-scope="scope">
                                {{ scope.row.name }} <br />
                                SKU: {{ scope.row.sku }} <br />
                                <b-badge variant="success" pill>
                                    #{{ scope.row.id }}
                                </b-badge>
                            </template>
                        </el-table-column>
                        <el-table-column label="在庫" sortable width="100" prop="rate">
                            <template slot-scope="scope">
                                <span class="d-block text-center">{{scope.row.inventory}}</span>
                                <a href="javascript:void(0);" class="btn btn-warning d-block" @click="InventoryOpt(scope.row, 'plus')">+</a>
                                <a href="javascript:void(0);" class="btn btn-danger d-block" @click="InventoryOpt(scope.row, 'minus')">-</a>
                            </template>
                        </el-table-column>
                        <el-table-column label="価格" sortable align="right" prop="is_valid">
                            <template slot-scope="scope">
                                <span class="d-block text-right">{{ scope.row.price | currency("¥") }}(販売)</span>
                                <span class="d-block text-right text-danger">
                                    {{scope.row.purchase_price | currency("- ¥")}}(仕入)
                                </span>
                                <span class="d-block text-right text-danger">{{ scope.row.extra_cost | currency("- ¥") }}(付加)</span>
                            </template>
                        </el-table-column>
                        <el-table-column label="Action">
                            <template slot-scope="scope">
                                <a v-b-modal.modal_variation_component href="javascript:void(0);" class="action-icon" @click="editVariation(scope.row)"><i class="fe-edit" />
                                </a>
                            </template>
                        </el-table-column>
                    </el-table>
                    <div v-if="variations_meta.total > 0" class="row my-2">
                        <div class="col">
                            <div class="dataTables_paginate paging_simple_numbers float-right">
                                <ul class="pagination pagination-rounded">
                                    <b-pagination v-model="variations_meta.page" pills aria-controls="pingoproduct_table" :total-rows="variations_meta.total" :per-page="variations_meta.page_size" @change="tablePageChange" />
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <VariationModal :showVariationModal="showVariationModal" :edit_variation="edit_variation" @operateresult="VariationOperate" />
</div>
</template>
