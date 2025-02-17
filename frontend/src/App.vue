<template>
  <div
    id="warningDiv"
    class="warning justify-center align-center"
    style="width: 100%; height: 100%; display: flex; justify-content: center; align-items: center"
  >
    <img src="/assets/power_ups/banana.png" class="trap" alt="Banana" />
    <img src="/assets/power_ups/bobomb.png" class="trap" alt="Bomb" />
    <img src="/assets/power_ups/mushroom.png" class="trap" alt="redShroom" />
    <img src="/assets/power_ups/goldmushroom.png" class="trap" alt="goldShroom" />
    <img src="/assets/power_ups/redshell.png" class="trap" alt="redShell" />
    <img src="/assets/power_ups/blueshell.png" class="trap" alt="blueShell" />
    <img src="/assets/power_ups/bolt.png" class="trap" alt="lightning" />
    <img src="/assets/power_ups/bill.png" class="trap" alt="bulletBill" />
  </div>
  <div class="bg-gray-800 h-screen">
    <div class="container mx-auto px-4 py-20 h-full">
      <div class="flex h-full">
        <!-- Map Section -->
        <div class="w-2/3 relative h-full bg-white">
          <div class="relative w-full h-full">
            <div class="flex justify-center items-center relative w-full h-full">
              <canvas id="countdownCanvas" width="400" height="400" class="absolute z-20"></canvas>
              <div class="flex justify-center items-center w-full h-full">
                <div class="slideshow w-full h-full flex justify-center items-center">
                  <img src="/assets/power_ups/banana.png" class="power-up" alt="Banana" />
                  <img src="/assets/power_ups/bobomb.png" class="power-up" alt="Bomb" />
                  <img src="/assets/power_ups/mushroom.png" class="power-up" alt="redShroom" />
                  <img src="/assets/power_ups/goldmushroom.png" class="power-up" alt="goldShroom" />
                  <img src="/assets/power_ups/redshell.png" class="power-up" alt="redShell" />
                  <img src="/assets/power_ups/blueshell.png" class="power-up" alt="blueShell" />
                  <img src="/assets/power_ups/bolt.png" class="power-up" alt="lightning" />
                  <img
                    src="/assets/power_ups/bill.png"
                    class="power-up h-[170px] max-h-[170px]"
                    alt="bulletBill"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- Info Section -->
        <div class="w-1/3 ml-8 overflow-auto my-auto">
          <div class="relative w-full h-full pb-10">
            <img src="/assets/map.png" alt="Map" class="w-full h-full" />
            <div
              v-for="kart in karts"
              :key="kart.id"
              class="absolute kart-head"
              :id="'kart-' + kart.id"
              :style="{
                top: scaleYLocation(kart.y) + '%',
                left: scaleXLocation(kart.x) + '%',
              }"
            >
              <img
                :src="'/assets/heads/' + kart.get_name() + '-head.png'"
                :alt="kart.get_name()"
                class="w-14 h-14"
              />
            </div>
          </div>
          <div
            v-for="(kart, index) in karts.slice(0, 3)"
            :key="kart.id"
            class="bg-white px-4 py-5 mb-4 rounded shadow flex items-center"
          >
            <span class="text-2xl font-bold mr-6">{{ index + 1 }}</span>
            <img :src="'/assets/heads/' + kart.get_name() + '-head.png'" class="w-8 h-8 mr-4" />
            <div class="flex justify-between w-full">
              <h2 class="text-2xl font-bold">{{ kart.get_name() }}</h2>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import Kart from "./Kart";
import { showTimer, showItem, showWarning, hidePowerUp, hideTimer, updateTimer } from "./script";

export default {
  setup() {
    const karts = ref([]);

    const map_height = 400;
    const map_width = 300;
    const scaleXLocation = (x) => {
      return (x / map_width) * 100;
    };
    const scaleYLocation = (y) => {
      return (y / map_height) * 100;
    };

    // Countdown

    let countDownDuration = 5000; // Total countdown time in miliseconds
    let countDownStart = 0;
    const trapImages = document.querySelectorAll(".warning img");
    const warningPopup = document.querySelectorAll(".warning");
    let timerVisible = false;
    let imageShowing = false;

    onMounted(() => {
      const canvas = document.getElementById("countdownCanvas");
      const ctx = canvas.getContext("2d");
      const powerUpImages = document.querySelectorAll(".slideshow img");

      let state = {
        countDownDuration: 10,
        countDownStart: 0,
        trapImages: trapImages,
        warningPopup: warningPopup,
        timerVisible: false,
        imageShowing: false,
        canvas: canvas,
        ctx: ctx,
        elapsedTime: 0.5,
        durationTime: 1,
        powerUpImages: powerUpImages,
      };

      const ws = new WebSocket("ws://localhost:8080");
      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log(data);
        const existingKart = karts.value.find((k) => k.id === data.id);
        if (existingKart) {
          existingKart.x = data.x;
          existingKart.y = data.y;
        } else {
          karts.value.push(new Kart(data.id, data.x, data.y));
        }
        if (data.msg === 1) {
          console.log("Item Pickup", data.item);
          showTimer(state);
          showItem(state, data.item);
          powerUpImages.forEach((img) => img.classList.remove("active"));
        }
      };
    });

    return { karts, scaleXLocation, scaleYLocation };
  },
};
</script>

<style>
.kart-head {
  position: absolute;
  transform: translate(-50%, -50%);
}
</style>
