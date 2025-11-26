document.addEventListener("DOMContentLoaded", function(){
        const BASE_URL = "http://127.0.0.1:8000";
        let brandNext = null, brandPrev = null;
        let modelNext = null, modelPrev = null;
        let fuelNext = null, fuelPrev = null;
        let gearNext = null, gearPrev = null;
        let carNext = null, carPrev = null;
        let orderings = [];

        function el(id){ return document.getElementById(id); }

        async function fetchJson(url){
            const res = await fetch(url);
            return await res.json();
        }

        function renderList(containerId, items, click){
            const c = el(containerId);
            c.innerHTML = "";
            const nextMap = { "brand-list": "brand-next", "model-list": "model-next", "fuel-list": "fuel-next", "gear-list": "gear-next" };
            const nextBtnId = nextMap[containerId];
            if (!items || items.length === 0) {
                const d = document.createElement("div");
                d.className = "empty";
                d.textContent = "Nenhum resultado";
                c.appendChild(d);
                if (nextBtnId && el(nextBtnId)) el(nextBtnId).style.display = "none";
                return;
            }
            if (nextBtnId && el(nextBtnId)) el(nextBtnId).style.display = "";
            items.forEach(v => {
                const d = document.createElement("div");
                d.className = "list-item";
                d.textContent = v;
                d.onclick = () => click(v);
                c.appendChild(d);
            });
        }

        async function loadBrands(url){
            const json = await fetchJson(url);
            const list = Array.isArray(json) ? json : json.results;
            const countEl = el("brand-count");
            if (countEl) countEl.textContent = `${list.length}`;
            renderList("brand-list", list, (v) => {
                el("car-brand").value = v;
                el("fuel-brand").value = v;
                el("gear-brand").value = v;
                el("p-brand").value = v;
                const b = encodeURIComponent(v);
                loadModels(`${BASE_URL}/api/v1/fipe/car/models/?page_size=10&brand=${b}`);
            });
            brandNext = json.next || null;
            brandPrev = json.previous || null;
            const bPrev = el("brand-prev");
            const bNext = el("brand-next");
            if (bPrev) bPrev.style.display = brandPrev ? "" : "none";
            if (bNext) bNext.style.display = brandNext ? "" : "none";
        }

        async function loadModels(url){
            const json = await fetchJson(url);
            const list = Array.isArray(json) ? json : json.results;
            const countEl = el("model-count");
            if (countEl) countEl.textContent = `${list.length}`;
            renderList("model-list", list, (v) => {
                el("car-model").value = v;
                el("fuel-model").value = v;
                el("gear-model").value = v;
                el("p-model").value = v;
                loadFuel();
                loadGear();
            });
            modelNext = json.next || null;
            modelPrev = json.previous || null;
            const mPrev = el("model-prev");
            const mNext = el("model-next");
            if (mPrev) mPrev.style.display = modelPrev ? "" : "none";
            if (mNext) mNext.style.display = modelNext ? "" : "none";
        }

        async function loadFuel(url){
            const brand = encodeURIComponent(el("fuel-brand").value);
            const model = encodeURIComponent(el("fuel-model").value);
            const base = `${BASE_URL}/api/v1/fipe/car/fuel_types/?page_size=10`;
            const full = `${base}${brand ? `&brand=${brand}`: ""}${model ? `&model=${model}`: ""}`;
            const json = await fetchJson(url || full);
            const list = Array.isArray(json) ? json : json.results;
            const countEl = el("fuel-count");
            if (countEl) countEl.textContent = `${list.length}`;
            renderList("fuel-list", list, (v) => {
                el("car-fuel").value = v;
                el("p-fuel").value = v;
            });
            fuelNext = json.next || null;
            fuelPrev = json.previous || null;
            const fPrev = el("fuel-prev");
            const fNext = el("fuel-next");
            if (fPrev) fPrev.style.display = fuelPrev ? "" : "none";
            if (fNext) fNext.style.display = fuelNext ? "" : "none";
        }

        async function loadGear(url){
            const brand = encodeURIComponent(el("gear-brand").value);
            const model = encodeURIComponent(el("gear-model").value);
            const base = `${BASE_URL}/api/v1/fipe/car/gear_types/?page_size=10`;
            const full = `${base}${brand ? `&brand=${brand}`: ""}${model ? `&model=${model}`: ""}`;
            const json = await fetchJson(url || full);
            const list = Array.isArray(json) ? json : json.results;
            const countEl = el("gear-count");
            if (countEl) countEl.textContent = `${list.length}`;
            renderList("gear-list", list, (v) => {
                el("car-gear").value = v;
                el("p-gear").value = v;
            });
            gearNext = json.next || null;
            gearPrev = json.previous || null;
            const gPrev = el("gear-prev");
            const gNext = el("gear-next");
            if (gPrev) gPrev.style.display = gearPrev ? "" : "none";
            if (gNext) gNext.style.display = gearNext ? "" : "none";
        }

        async function loadCars(url){
            const brand = encodeURIComponent(el("car-brand").value);
            const model = encodeURIComponent(el("car-model").value);
            const fuel = encodeURIComponent(el("car-fuel").value);
            const gear = encodeURIComponent(el("car-gear").value);
            const year = encodeURIComponent(el("car-year").value);
            const engine = encodeURIComponent(el("car-engine").value);
            const orderingParam = orderings.join(",");
            const base = `${BASE_URL}/api/v1/fipe/car/?page_size=12`;
            const full = `${base}` +
                `${brand ? `&brand=${brand}`:""}` +
                `${model ? `&model=${model}`:""}` +
                `${fuel ? `&fuel_type=${fuel}`:""}` +
                `${gear ? `&gear_type=${gear}`:""}` +
                `${year ? `&year=${year}`:""}` +
                `${engine ? `&engine_size=${engine}`:""}` +
                `${orderingParam ? `&ordering=${encodeURIComponent(orderingParam)}`:""}`;
            const json = await fetchJson(url || full);
            const list = json.results || [];
            const container = el("car-list");
            container.innerHTML = "";
            if (!list.length) {
                const d = document.createElement("div");
                d.className = "empty";
                d.textContent = "Nenhum resultado";
                container.appendChild(d);
                const nextBtn = el("car-next");
                if (nextBtn) nextBtn.style.display = "none";
            } else {
                const nextBtn = el("car-next");
                if (nextBtn) nextBtn.style.display = "";
            }
            list.forEach(car => {
                const d = document.createElement("div");
                d.className = "car-item";
                d.innerHTML = `<div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="font-weight:600;padding-bottom:6px;">${car.brand} ${car.model}</div>
                        <div class="badge">${car.year}</div>
                        <div class="badge">${car.fuel_type}</div>
                        <div class="badge">${car.gear_type}</div>
                        <div class="badge">${car.engine_size}</div>
                    </div>
                    <div style="font-weight:700; color:#aaf581;">R$ ${car.price.toLocaleString()}</div>
                </div>`;
                container.appendChild(d);
            });
            carNext = json.next || null;
            carPrev = json.previous || null;
        }

        async function predict(){
            const btn = el("predict-btn");
            const box = el("prediction-result");
            const originalText = btn.textContent;
            btn.textContent = "Prevendo...";
            btn.disabled = true;
            box.style.display = "block";
            box.innerHTML = "Calculando...";
            const data = {
                year: el("p-year").value,
                engine: el("p-engine").value,
                brand: el("p-brand").value,
                model: el("p-model").value,
                fuel: el("p-fuel").value,
                gear: el("p-gear").value,
            };
            try {
                const res = await fetch(`${BASE_URL}/api/v1/predict/car/`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) });
                const json = await res.json();
                box.style.display = "block";
                box.innerHTML = `Preço Previsto: R$ ${json.prediction.toLocaleString("pt-BR", { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`;
            } catch (e) {
                box.style.display = "block";
                box.innerHTML = "Falha ao obter previsão";
            } finally {
                btn.textContent = originalText;
                updatePredictButtonState();
            }
        }

        function populateYears(){
            ["p-year","car-year"].forEach(id => {
                const select = el(id);
                if (!select) return;
                select.innerHTML = "<option value=''>Selecione o ano</option>";
                const current = new Date().getFullYear();
                for (let y = current; y >= 1970; y--) {
                    const opt = document.createElement("option");
                    opt.value = String(y);
                    opt.textContent = String(y);
                    select.appendChild(opt);
                }
                select.value = String(current);
            });
        }

        function isPredictReady(){
            return (
                !!el("p-year").value &&
                !!el("p-engine").value &&
                !!el("p-brand").value &&
                !!el("p-model").value &&
                !!el("p-fuel").value &&
                !!el("p-gear").value
            );
        }

        function updatePredictButtonState(){
            el("predict-btn").disabled = !isPredictReady();
        }

        el("brand-next").onclick = () => { if (brandNext) loadBrands(brandNext); };
        el("brand-prev").onclick = () => { if (brandPrev) loadBrands(brandPrev); };
        el("model-next").onclick = () => { if (modelNext) loadModels(modelNext); };
        el("model-prev").onclick = () => { if (modelPrev) loadModels(modelPrev); };
        el("fuel-next").onclick = () => { if (fuelNext) loadFuel(fuelNext); };
        el("fuel-prev").onclick = () => { if (fuelPrev) loadFuel(fuelPrev); };
        el("gear-next").onclick = () => { if (gearNext) loadGear(gearNext); };
        el("gear-prev").onclick = () => { if (gearPrev) loadGear(gearPrev); };
        el("car-next").onclick = () => { if (carNext) loadCars(carNext); };
        el("car-prev").onclick = () => { if (carPrev) loadCars(carPrev); };
        el("car-load").onclick = () => loadCars();
        el("car-clear").onclick = () => { el("car-brand").value = ""; el("car-model").value = ""; el("car-fuel").value = ""; el("car-gear").value = ""; el("car-year").value = ""; el("car-engine").value = ""; orderings = []; document.querySelectorAll('#car-order-chips .chip').forEach(ch => ch.classList.remove('selected')); loadCars(); };
        document.querySelectorAll('#car-order-chips .chip').forEach(chip => {
            chip.addEventListener('click', () => {
                const val = chip.dataset.order;
                const field = val.replace('-', '');
                const asc = field;
                const desc = '-' + field;
                const hasAsc = orderings.includes(asc);
                const hasDesc = orderings.includes(desc);
                if (orderings.includes(val)) {
                    orderings = orderings.filter(v => v !== val);
                    chip.classList.remove('selected');
                } else {
                    if (hasAsc && val === desc) {
                        orderings = orderings.filter(v => v !== asc);
                        document.querySelector(`#car-order-chips .chip[data-order="${asc}"]`)?.classList.remove('selected');
                    }
                    if (hasDesc && val === asc) {
                        orderings = orderings.filter(v => v !== desc);
                        document.querySelector(`#car-order-chips .chip[data-order="${desc}"]`)?.classList.remove('selected');
                    }
                    orderings.push(val);
                    chip.classList.add('selected');
                }
                loadCars();
            });
        });
        el("predict-btn").onclick = () => predict();
        ["p-year","p-engine","p-brand","p-model","p-fuel","p-gear"].forEach(id => {
            el(id).addEventListener("input", updatePredictButtonState);
            el(id).addEventListener("change", updatePredictButtonState);
        });
        ["brand-list","model-list","fuel-list","gear-list"].forEach(id => {
            el(id).addEventListener("click", updatePredictButtonState);
        });

        el("brand-search").addEventListener("input", (e) => {
            const q = e.target.value.trim();
            const url = `${BASE_URL}/api/v1/fipe/car/brands/?page_size=10${q ? `&q=${encodeURIComponent(q)}`: ""}`;
            loadBrands(url);
        });
        el("model-search").addEventListener("input", (e) => {
            const q = e.target.value.trim();
            const brand = encodeURIComponent(el("car-brand").value);
            const base = `${BASE_URL}/api/v1/fipe/car/models/?page_size=10`;
            const url = `${base}${brand ? `&brand=${brand}`: ""}${q ? `&q=${encodeURIComponent(q)}`: ""}`;
            loadModels(url);
        });

        loadBrands(`${BASE_URL}/api/v1/fipe/car/brands/?page_size=10`);
        loadModels(`${BASE_URL}/api/v1/fipe/car/models/?page_size=10`);
        populateYears();
        loadFuel();
        loadGear();
        loadCars();
        updatePredictButtonState();
});
