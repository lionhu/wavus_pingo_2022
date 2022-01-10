<script>
/**
 * Auth-2 layout
 */
export default {
  name:"layout_auth",
    mounted() {
        document.body.classList.add('auth-fluid-pages')
    }
}
</script>

<template>
<div class="auth-fluid">
    <!-- Auth fluid right content -->
    <div class="auth-fluid-right">
        <div class="auth-user-testimonial">
            <h3 class="mb-3 text-white">Very elegant & impressive!</h3>
            <p class="lead font-weight-normal"><i class="mdi mdi-format-quote-open"></i> This is the EC-Shopping site what I am looking for. Not only high cost performance, but also fun to share with friends. I would highly recommend Pingo.jp <i class="mdi mdi-format-quote-close"></i>
            </p>
            <h5 class="text-white">
                - Lily Takahashi
            </h5>
        </div> <!-- end auth-user-testimonial-->
    </div>
    <!-- end Auth fluid right content -->

    <!--Auth fluid left content -->
    <div class="auth-fluid-form-box">
        <div class="align-items-center d-flex h-100">
            <div class="card-body">
                <Nuxt />
            </div>
        </div>
    </div>
</div>
</template>
