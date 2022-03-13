<script>
import {
    mapGetters
} from 'vuex'
import Swal from 'sweetalert2'
import {
    APIServices
} from '@/helpers/APIs'
import {
    swalService
} from '~/helpers/swal.service'

export default {
    name: 'EditProductVariationTable',
    components: {
        'el-upload': () => import('element-ui/lib/upload'),
        VariationModal: () => import('./VariationModal')
    },
    props: {
        variations: Array,
        product_id: Number
    },
    data() {
        return {
            showVariationModal: false,
            modeAdd: false,
            edit_variation: {
                price: 0,
                purchase_price: 0,
                name: '',
                description: '',
                variation_type: 'REGULAR',
                inventory: 0,
                sort_by: 0,
                point_rule: {
                    is_valid: false,
                    type: 'amount',
                    policies: {
                        client_superadmin: 0,
                        client_admin: 0,
                        level_2: 0,
                        level_1: 0,
                        user_self: 0
                    },
                    special_promotion: {
                        is_valid: false,
                        bonus: 0
                    }
                }
            }
        }
    },
    computed: {
        ...mapGetters({
            // suppliers: "suppliers/getterSupplierList",
            // categories: "categories/getProductCategories",
        }),
        csrftoken () {
            return this.$auth.strategy.token.get()
        }
    },
    methods: {
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
            this.modeAdd = true
            this.showVariationModal = true
        },
        deleteVariation(variationId) {
            this.$emit('operateTable', {
                command: 'deleteVariation',
                variation: variationId
            })
        },

        editVariation(variation) {
            this.edit_variation = variation
            this.modeAdd = false
            this.showVariationModal = true
        },

        getUploadVariationimageURL(id) {
            return `https://www.pingo.jp/daphne/api/store/public/variations/${id}/update_image/`
        },
        beforeAvatarUpload(file) {
            const isJPG = file.type === 'image/jpeg'
            const isLt2M = file.size / 1024 / 1024 < 2
            // return isLt2M;
            if (!isLt2M || !isJPG) {
                swalService.showModal(
                    'Invalid picture',
                    'Should be JPEG and below 2M',
                    'warning'
                )
                return false
            }
            return isJPG && isLt2M
            // return isJPG && isLt2M;
        },
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        handleVariationImageSuccess(res, file) {
            if (res.result) {
                this.$emit('operateTable', {
                    command: 'replaceVariation',
                    variation: res.data
                })
            }
        },

        VariationOperate({
            modeAdd,
            _variation
        }) {
            const vm = this
            if (!modeAdd) {
                this.$emit('operateTable', {
                    command: 'editVariation',
                    variation: _variation
                })
                // }
            } else {
                this.$emit('operateTable', {
                    command: 'addVariation',
                    variation: _variation
                })
            }
            vm.showVariationModal = false
        }
    }
}
</script>
<template>
<div>
    <div class="card">
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    登録したバリエーション
                </div>
                <div class="col-md-6">
                    <button v-b-modal.modal_variation_component class="btn btn-warning mb-2 float-right" @click="switchAddVariationMode">
                        <i class="mdi mdi-plus-circle mr-1" /> バリエーションの追加
                    </button>
                </div>
            </div>
            <div class="row">
                <div class="table-responsive">
                    <table class="table table-bordered table-centered mb-0">
                        <thead class="thead-light">
                            <tr>
                                <th>商品名</th>
                                <th>順番</th>
                                <th>在庫</th>
                                <th>販売価格 <br>仕入価格<br>付加コスト</th>
                                <th>ポイントポリシー</th>
                                <th />
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="variation in variations" :key="variation.id">
                                <td class="text-center">
                                    <font-awesome-icon :icon="['fa', 'award']" :class="{
                        'text-success': variation.is_valid,
                        'text-danger': !variation.is_valid,
                      }" />{{ variation.name }} <br>

                                    <b-badge v-if="variation.variation_type === 'REGULAR'" variant="primary" pill>
                                        REGULAR (#{{ variation.id }})
                                    </b-badge>
                                    <b-badge v-else variant="warning" pill>
                                        Pingo (#{{ variation.id }})
                                    </b-badge>
                                    <br>
                                    <b-badge v-if="variation.is_valid" variant="primary" pill>
                                        <font-awesome-icon :icon="['fa', 'award']" />
                                        Valid
                                    </b-badge>
                                    <b-badge v-else variant="danger" pill>
                                        <font-awesome-icon :icon="['fa', 'award']" />
                                        inValid
                                    </b-badge>

                                    <el-upload class="avatar-uploader" :action="getUploadVariationimageURL(variation.id)" :show-file-list="false" :headers="{ Authorization: csrftoken }" :on-success="handleVariationImageSuccess" :name="'image'" :before-upload="beforeAvatarUpload">
                                        <img v-if="variation.image_url" :src="variation.image_url" class="avatar">
                                        <i v-else class="el-icon-plus avatar-uploader-icon" />
                                    </el-upload>
                                </td>
                                <td class="text-center">
                                    <b-badge variant="danger" pill>
                                        {{ variation.sort_by }}
                                    </b-badge>
                                </td>
                                <td class="text-center">
                                    <span class="d-block">{{ variation.inventory }}</span>
                                    <a href="javascript:void(0);" class="btn btn-warning d-block" @click="InventoryOpt(variation, 'plus')">+</a>
                                    <a href="javascript:void(0);" class="btn btn-danger d-block" @click="InventoryOpt(variation, 'minus')">-</a>
                                </td>
                                <td class="text-right">
                                    <span class="d-block">{{
                      variation.price | currency("¥")
                    }}</span>
                                    <span class="d-block text-danger">{{
                      variation.purchase_price | currency("- ¥")
                    }}</span>
                                    <span class="d-block text-danger">{{
                      variation.extra_cost | currency("- ¥")
                    }}</span>
                                </td>
                                <td class="text-right">
                                    <h5>
                                        <span class="d-inline-block float-left">紹介ポイント</span>
                                        <b-badge v-if="variation.point_rule.is_valid" variant="success float-right" pill>
                                            on
                                        </b-badge>
                                        <b-badge v-else variant="danger float-right" pill>
                                            off
                                        </b-badge>
                                    </h5>
                                    <div class="clearfix" />
                                    <ul v-if="variation.point_rule.is_valid" style="list-style-type: none">
                                        <li>
                                            <span class="inline-block text-right mr-3">{{
                          $t(
                            "menuitems.organizations.user.client_superadmin"
                          )
                        }}:</span>
                                            {{
                          variation.point_rule.policies.client_superadmin
                            | currency("¥")
                        }}
                                        </li>
                                        <li>
                                            <span class="inline-block text-right mr-3">{{
                          $t("menuitems.organizations.user.client_admin")
                        }}:</span>
                                            {{
                          variation.point_rule.policies.client_admin
                            | currency("¥")
                        }}
                                        </li>
                                        <li>
                                            <span class="inline-block text-right mr-3">{{
                          $t("menuitems.organizations.user.level_2")
                        }}:</span>{{
                          variation.point_rule.policies.level_2 | currency("¥")
                        }}
                                        </li>
                                        <li>
                                            <span class="inline-block text-right mr-3">{{
                          $t("menuitems.organizations.user.level_1")
                        }}:</span>{{
                          variation.point_rule.policies.level_1 | currency("¥")
                        }}
                                        </li>
                                        <li>
                                            <span class="inline-block text-right mr-3">{{
                          $t("menuitems.organizations.user.user_self")
                        }}:</span>{{
                          variation.point_rule.policies.user_self
                            | currency("¥")
                        }}
                                        </li>
                                    </ul>
                                </td>
                                <td class="align-items-center">
                                    <a v-b-modal.modal_variation_component href="javascript:void(0);" class="action-icon" @click="editVariation(variation)">
                                        <i class="fe-edit" /></a>
                                    <a href="javascript:void(0);" class="action-icon" @click="deleteVariation(variation.id)">
                                        <i class="fe-trash" /></a>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
    <VariationModal :show-variation-modal="showVariationModal" :mode-add="modeAdd" :edit_variation="edit_variation" :product_id="product_id" @operateresult="VariationOperate" />
</div>
</template>
