<template>
  <div>
    <div>
      <!-- Page Content -->
    <div class="container">

      <!-- Page Heading -->
      <h1 class="my-4">Rent objects in Kyiv</h1>
      <p><i>Find the best place for long-term living in Kyiv, Ukraine!</i></p>

      <div class="row">
        <div class="col-md-5">
          <div class="panel panel-default">
            <div class="panel-body">
                <form class="form-inline" role="form">
                    <div class="form-group">
                        <label class="filter-col mr-1" for="pref-search">Search: </label>
                        <input type="text" class="form-control input-sm" id="pref-search" v-model="searchParams.search">
                    </div>
                    <div class="form-group pl-2">
                        <label class="filter-col mr-1" for="pref-perpage">Rooms:</label>
                        <select id="pref-perpage" class="form-control" v-model="searchParams.rooms">
                            <option value="1">1</option>
                            <option value="2">2</option>
                            <option value="3">3</option>
                            <option value="4">4</option>
                            <option value="5">5</option>
                        </select>
                    </div>
                    <div class="form-group pt-2">
                        <label class="filter-col mr-1" for="pref-orderby">
                        Order by:
                        </label>
                        <select id="pref-orderby" class="form-control" v-model="searchParams.orderBy" @change="search()">
                          <option value="date">▼ Date</option>
                          <option value="-date">▲ Date</option>
                          <option value="-price">▼ Price</option>
                          <option value="price">▲ Price</option>
                        </select>
                    </div>
                    <div class="form-group pt-2 pl-2">
                        <label class="filter-col mr-2" for="pref-perpage">City district:</label>
                        <select class="form-control" v-model="searchParams.cityDistrict">
                            <option v-for="district in cityDisctricts" :value="district.id" :key="district.id">{{ district.title }}</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="filter-col" for="pref-search">Price, uah:</label>
                        <input type="text" class="form-control input-sm m-2 w-25" placeholder="min:" v-model="searchParams.lowPrice">
                        <input type="text" class="form-control input-sm m-2 w-25" placeholder="max:" v-model="searchParams.highPrice">
                    </div>
                    <button class="btn btn-primary" @click="search()">Search</button>
                </form>
            </div>
          </div>
        </div>
      </div>
      <span><strong>{{ count }}</strong> objects found</span>
      <hr/>

      <!-- rent object list -->
      <div v-for="rentObject in rentObjects" :key="rentObject.id">
        <div class="row">
          <div class="col-md-3">
            <a href="#">
              <img class="img-fluid rounded mb-3 mb-md-0" src="http://placehold.it/300x200" alt="">
            </a>
          </div>
          <div class="col-md-5">
            <h3 class="link-text"><a target="_blank" :href="rentObject.url">{{ rentObject.shortTitle }}</a></h3>
            <span><b class="price-text">{{ rentObject.price }} uah</b></span>
            <p>{{ processRentDescription(rentObject.text) }}</p>
          </div>
        </div>
        <!-- /.row -->
        <hr>
      </div>

    <div v-if="count > 20">
      <paginate
        :page-count="pagesCount"
        :click-handler="changePage"
        :page-range="2"
        :margin-pages="2"
        :prev-text="'Prev'"
        :next-text="'Next'"
        :prev-class="'page-item page-link'"
        :next-class="'page-item page-link'"
        :container-class="'pagination justify-content-center'"
        :page-class="'page-item page-link'">
      </paginate>
    </div>
    </div>
    <!-- /.container -->
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Home',
  data () {
    return {
      rentObjects: [],
      searchParams: {
        search: null,
        orderBy: null,
        lowPrice: null,
        highPrice: null,
        rooms: null,
        cityDistrict: null,
        page: null
      },
      count: null,
      pagesCount: null,
      cityDisctricts: []
    }
  },

  methods: {
    getRentObjects () {
      let params = {}

      for (let property in this.searchParams) {
        if (this.searchParams[property]) {
          params[property] = this.searchParams[property]
        }
      }
      this.$router.replace({query: params})
      axios.get(`${process.env.API_ROOT}api/rent-objects`, {params: params})
        .then((res) => {
          this.rentObjects = res.data.data
          this.count = res.data.count
          this.pagesCount = Math.floor(this.count / 20)
        })
        .catch((error) => {
          console.error(error)
        })
    },

    search () {
      this.searchParams.page = 1
      this.getRentObjects()
    },

    changePage (page) {
      this.searchParams.page = page
      this.getRentObjects()
    },

    getCityDistricts () {
      axios.get(`${process.env.API_ROOT}api/city-districts`)
        .then((res) => {
          this.cityDisctricts = res.data
        })
        .catch((error) => {
          console.error(error)
        })
    },

    processRentDescription (text) {
      return text ? text.substring(0, 207) + '...' : 'No description'
    }
  },

  created () {
    this.searchParams = this.$route.query
    this.getRentObjects()
    this.getCityDistricts()
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

  .price-text {
    font-size: 22px;
    color: #3c9806;
  }

  .link-text {
    font-size: 18px;
    color: #256799;
  }

</style>
