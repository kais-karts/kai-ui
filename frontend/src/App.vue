<template>
  <!-- Warning Section -->
  <div
    id="warningDiv"
    class="warning justify-center items-center"
    style="width: 100%; height: 100%; display: none; align-items: center"
  >
    <img src="/assets/power_ups/banana.png" class="trap" alt="Banana" id="trap-0" />
    <img src="/assets/power_ups/bobomb.png" class="trap" alt="Bomb" id="trap-1" />
    <img src="/assets/power_ups/mushroom.png" class="trap" alt="redShroom" id="trap-2" />
    <img src="/assets/power_ups/bolt.png" class="trap" alt="lightning" id="trap-3" />
    <img src="/assets/power_ups/bill.png" class="trap" alt="bulletBill" id="trap-4" />
    <img src="/assets/power_ups/goldmushroom.png" class="trap" alt="goldShroom" id="trap-5" />
    <img src="/assets/power_ups/redshell.png" class="trap" alt="redShell" id="trap-6" />
    <img src="/assets/power_ups/blueshell.png" class="trap" alt="blueShell" id="trap-7" />
  </div>

  <!-- Main UI -->
  <div class="bg-gray-800 h-screen z-10">
    <div class="container mx-auto px-4 py-10 h-full">
      <div class="flex h-full">
        <!-- Map & Timer Section -->
        <div class="w-3/5 relative h-full bg-slate-600 rounded-2xl">
          <div class="relative w-full h-full">
            <div class="flex justify-center items-center relative w-full h-full">
              <canvas id="countdownCanvas" width="400" height="400" class="absolute z-20"></canvas>
              <div class="flex justify-center items-center w-full h-full">
                <div class="slideshow w-full h-full flex justify-center items-center">
                  <img src="/assets/power_ups/banana.png" class="power-up" id="spinner-0" />
                  <img src="/assets/power_ups/bobomb.png" class="power-up" id="spinner-1" />
                  <img src="/assets/power_ups/mushroom.png" class="power-up" id="spinner-2" />
                  <img src="/assets/power_ups/bolt.png" class="power-up" id="spinner-3" />
                  <img
                    src="/assets/power_ups/bill.png"
                    class="power-up h-[170px] max-h-[170px]"
                    id="spinner-4"
                  />
                  <img src="/assets/power_ups/goldmushroom.png" class="power-up" id="spinner-5" />
                  <img src="/assets/power_ups/redshell.png" class="power-up" id="spinner-6" />
                  <img src="/assets/power_ups/blueshell.png" class="power-up" id="spinner-7" />

                  <img
                    src="/assets/power_ups/no-item.png"
                    style="display: block; object-fit: contain"
                    id="no-item"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Info Section -->
        <div class="w-2/5 ml-8 overflow-hidden">
          <div class="relative w-full h-3/5 mb-10">
            <img src="/assets/map.png" alt="Map" class="w-full h-full rounded-lg" />
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
          <div class="h-2/5 flex flex-col">
            <div
              v-for="(kart, index) in ranked_karts"
              :key="kart.id"
              class="bg-slate-500 px-4 py-5 mb-4 rounded shadow flex items-center"
            >
              <span class="text-2xl font-bold mr-6">{{ index + 1 }}</span>
              <img :src="'/assets/heads/' + kart.get_name() + '-head.png'" class="w-8 h-8 mr-4" />
              <div class="flex justify-between w-full">
                <h2 class="text-2xl font-bold">{{ kart.get_title() }}</h2>
              </div>
            </div>
          </div>
          <!-- <button class="bg-slate-300" @click="recieve_item()">Recieve Item</button>
          <button class="bg-slate-300" @click="use_buff()">Use buff</button>
          <button class="bg-slate-300" @click="send_debuff()">Send debuff</button>
          <button class="bg-slate-300 text-white" @click="get_hit()">Get Hit</button> -->
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import Kart from "./kart.js";

export default {
  setup() {
    const karts = ref([]);
    const ranked_karts = ref([]);

    // Map scaling helpers
    const map_height = 400;
    const map_width = 300;
    const scaleXLocation = (x) => (x / map_width) * 100;
    const scaleYLocation = (y) => (y / map_height) * 100;

    // Countdown / Power-Up variables
    let countDownDuration = 5000; // in ms
    let countDownStart = 0;
    let timerVisible = false;
    let imageShowing = false;
    let slideshowIndex = 0;

    // These DOM elements will be set in onMounted
    let canvas, ctx, powerUpImages, trapImages, noItemImage;

    // For item to number mapping
    const ITEMMAP = {
      0: "banana",
      1: "bobomb",
      2: "redShroom",
      3: "lightning",
      4: "bulletBill",
      5: "goldShroom",
      6: "redShell",
      7: "blueshell",
    };
    const SELF_KART_ID = Kart.get_self_kart_id();

    // -------------------------------
    // Timer & Arc Drawing Functions
    // -------------------------------
    function drawArc(elapsedTime, durationTime) {
      console.log("drawArc", elapsedTime, durationTime);
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.beginPath();
      const percentage = durationTime === 0 ? 0 : elapsedTime / durationTime;
      ctx.arc(
        canvas.width / 2,
        canvas.height / 2,
        170,
        1.5 * Math.PI,
        1.5 * Math.PI + 2 * Math.PI * percentage,
        true
      );
      ctx.lineWidth = 18;
      ctx.strokeStyle = "#2B7FFF";
      ctx.stroke();
      ctx.closePath();
      console.log(1.5 * Math.PI, 1.5 * Math.PI + 2 * Math.PI * percentage);
    }

    function updateTimer() {
      let elapsed = new Date().getTime() - countDownStart;
      if (elapsed < countDownDuration && timerVisible) {
        console.log(elapsed, countDownDuration, countDownStart);
        drawArc(elapsed, countDownDuration);
        requestAnimationFrame(updateTimer);
      } else {
        hideTimer();
        hidePowerUp();
        console.log("Countdown finished!");
        noItemImage.style.display = "block";
      }
    }

    function showTimer() {
      console.log("show timer");
      drawArc(0.0001, 1);
      timerVisible = true;
      countDownStart = new Date().getTime();
    }

    function hideTimer() {
      console.log("hide timer");
      drawArc(1, 1);
      timerVisible = false;
    }

    // -------------------------------
    // Power-Up Slideshow Functions
    // -------------------------------
    function hidePowerUp() {
      powerUpImages.forEach((img) => img.classList.remove("active"));
    }

    function changeImage() {
      powerUpImages.forEach((img) => img.classList.remove("active"));
      slideshowIndex = (slideshowIndex + 1) % powerUpImages.length;
      powerUpImages[slideshowIndex].classList.add("active");
    }

    function showItem(itemIndex) {
      console.log("show item");
      let startTime = new Date().getTime();
      let intervalId = setInterval(() => {
        changeImage();
        if (new Date().getTime() - startTime >= 1000) {
          clearInterval(intervalId);
          powerUpImages.forEach((img) => img.classList.remove("active"));
          if (powerUpImages[itemIndex]) {
            powerUpImages[itemIndex].classList.add("active");
          }
        }
      }, 100);
    }

    // -------------------------------
    // Warning / Trap Functions
    // -------------------------------
    function blinkImage(item) {
      if (imageShowing) {
        trapImages[item].classList.remove("active");
      } else {
        trapImages[item].classList.add("active");
      }
      imageShowing = !imageShowing;
    }

    function showWarning(item, duration) {
      hidePowerUp();
      hideTimer();
      console.log("incoming item");
      let startTime = new Date().getTime();
      let intervalId = setInterval(() => {
        document.getElementById("warningDiv").style.display = "flex";
        blinkImage(item);
        if (new Date().getTime() - startTime >= duration * 1000) {
          clearInterval(intervalId);
          console.log(trapImages[item]);
          trapImages[item].classList.remove("active");
          document.getElementById("warningDiv").style.display = "none";
        }
      }, 100);
    }

    // -------------------------------
    // Simulated "Receive Item" Function
    // -------------------------------
    // This function is called when the button is clicked.
    // It simulates receiving an item (in this example, "banana" at index 0).
    // const recieve_item = () => {
    //   const data = { item: 0, item_type: "debuff" };

    //   console.log("Pick up Item", data.item);
    //   noItemImage.style.display = "none";
    //   if (data.item_type === "buff") {
    //     showTimer();
    //     showItem(data.item);
    //     hidePowerUp();
    //   } else if (data.item_type === "debuff") {
    //     document.getElementById("spinner-" + data.item).classList.add("active");
    //   }
    // };

    // const use_buff = () => {
    //   console.log("Item Use", "banana");
    //   if (timerVisible) {
    //     countDownStart = new Date().getTime();
    //     countDownDuration = 5 * 1000;
    //     updateTimer();
    //   }
    // };

    // const send_debuff = () => {
    //   console.log("Send Debuff", "banana");
    //   hidePowerUp();
    //   noItemImage.style.display = "block";
    // };

    // const get_hit = () => {
    //   showWarning(1, 10);
    // };

    // -------------------------------
    // WebSocket & DOM Initialization
    // -------------------------------
    onMounted(() => {
      ranked_karts.value = [
        new Kart(1, 100, 100, 0),
        new Kart(2, 200, 200, 1),
        new Kart(3, 250, 300, 2),
      ];

      karts.value = ranked_karts.value;

      // Get canvas & context for countdown
      canvas = document.getElementById("countdownCanvas");
      ctx = canvas.getContext("2d");

      // Select images from the slideshow & warning sections
      powerUpImages = document.querySelectorAll(".slideshow img:not(#no-item)");
      trapImages = document.querySelectorAll(".warning img:not(#no-item)");
      noItemImage = document.getElementById("no-item");

      console.log(trapImages);
      console.log(powerUpImages);
      console.log(noItemImage);

      // Setup WebSocket connection (adjust URL/port as needed)
      const wss = new WebSocket("ws://localhost:5000");
      console.log("WebSocket connecting...");
      wss.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log("WebSocket data:", data);

        // Handle different actions sent over WebSocket
        if (data.action === "item_pickup") {
          console.log("Pick up Item", data.item);
          noItemImage.style.display = "none";
          if (data.item_type === "buff") {
            showTimer();
            showItem(data.item);
            hidePowerUp();
          } else if (data.item_type === "debuff") {
            document.getElementById("spinner-" + data.item).classList.add("active");
          }
        } else if (data.action === "use_buff") {
          console.log("Item Use", data.item);
          if (timerVisible) {
            countDownStart = new Date().getTime();
            countDownDuration = data.duration * 1000;
            updateTimer();
          }
        } else if (data.action === "send_debuff") {
          console.log("Send Debuff", data.item);
          hidePowerUp();
          noItemImage.style.display = "block";
        } else if (data.action === "item_hit") {
          console.log("Hit by item", data.item);
          showWarning(data.item, data.duration);
        } else if (data.action === "players_update") {
          console.log("Item Use", data.item);
          // Update or add kart data based on incoming coordinates
          data.players_update.forEach((player) => {
            const existingKart = karts.find((k) => k.id === player.id);
            if (existingKart) {
              existingKart.x = player.x;
              existingKart.y = player.y;
              existingKart.ranking = player.ranking;
            } else {
              karts.push(new Kart(player.id, player.x, player.y, player.ranking));
            }
          });
          // return first 3 karts by ranking
          karts.sort((a, b) => a.ranking - b.ranking);
          ranked_karts = karts.slice(0, 3);
          if (!ranked_karts.some((kart) => kart.id === SELF_KART_ID)) {
            const globalKart = karts.find((kart) => kart.id === SELF_KART_ID);
            if (globalKart) {
              ranked_karts[2] = globalKart;
            }
          }
        }
      };
    });

    return {
      karts,
      ranked_karts,
      scaleXLocation,
      scaleYLocation,
    };
  },
};
</script>

<style scoped>
.kart-head {
  position: absolute;
  transform: translate(-50%, -50%);
}

/* Optional styling for smoother transitions */
.warning img,
.slideshow img {
  transition: opacity 0.3s ease;
}
.warning img,
.slideshow img {
  opacity: 0.3;
}
.warning img.active,
.slideshow img.active {
  opacity: 1;
}
</style>
