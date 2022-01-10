import {APIServices} from '~/helpers/APIs';

export const categoryService = {
  getAll,
  update,
  insert,
  remove
};
const urls = {
  "list": "store/public/categories/",
}


function getAll() {
  return APIServices.get(urls.list)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}

function  remove(category_id) {
  let url=`${urls.list}${category_id}/`

  return APIServices.destroy(url)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}
function update(category) {
  let url=`${urls.list}${category.id}/`
  console.log( category)
  delete category.id;
  if (Object.keys(category).includes("regular_product_count")){
    delete category.regular_product_count;
  }
  if (Object.keys(category).includes("pingo_product_count")){
    delete category.pingo_product_count;
  }
  console.log("updated category",url, category)

  return APIServices.put(url,category)
    .then(APIServices.handleResponse)
    .then(response => {
      return response;
    });
}

function insert(category) {
    return APIServices.post(urls.list,category)
      .then(APIServices.handleResponse)
      .then(response => {
        return response;
      });
}
