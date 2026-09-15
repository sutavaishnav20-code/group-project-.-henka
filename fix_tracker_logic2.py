import re

with open("index.html", "r") as f:
    content = f.read()

tracker_vars_pattern = r"let repCount = 0;[\s\S]*?let trackerPose = null;"

tracker_vars_new = """let repCount = 0;
        let exerciseStage = "down"; 
        let isGoodForm = true;
        let trackerCamera = null;
        let trackerPose = null;
        
        let timerStart = 0;
        let currentDuration = 0;
        let isHolding = false;
        let weeklyData = JSON.parse(localStorage.getItem('henkaWeeklyData') || '[]');
        
        if (weeklyData.length === 0) {
            const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
            weeklyData = days.map(d => ({ day: d, value: Math.floor(Math.random() * 20) + 5 }));
            localStorage.setItem('henkaWeeklyData', JSON.stringify(weeklyData));
        }

        window.renderChart = function() {
            if (typeof d3 === 'undefined') return;
            d3.select('#d3Chart').selectAll('*').remove();
            
            const chartContainer = document.getElementById('d3Chart');
            if (!chartContainer) return;
            
            const margin = {top: 10, right: 10, bottom: 20, left: 30};
            const width = chartContainer.clientWidth - margin.left - margin.right;
            const height = 200 - margin.top - margin.bottom;

            const svg = d3.select('#d3Chart')
              .append('svg')
                .attr('width', width + margin.left + margin.right)
                .attr('height', height + margin.top + margin.bottom)
              .append('g')
                .attr('transform', `translate(${margin.left},${margin.top})`);

            const x = d3.scalePoint()
              .domain(weeklyData.map(d => d.day))
              .range([0, width])
              .padding(0.5);

            const y = d3.scaleLinear()
              .domain([0, d3.max(weeklyData, d => d.value) * 1.2 || 10])
              .range([height, 0]);

            svg.append('g')
              .attr('transform', `translate(0,${height})`)
              .call(d3.axisBottom(x).tickSize(0).tickPadding(8))
              .call(g => g.select('.domain').attr('stroke', 'var(--line)'))
              .selectAll('text').attr('fill', 'var(--ink-faint)');

            svg.append('g')
              .call(d3.axisLeft(y).ticks(4).tickSize(-width))
              .call(g => g.select('.domain').remove())
              .call(g => g.selectAll('.tick line').attr('stroke', 'var(--line)').attr('stroke-dasharray', '2,2'))
              .selectAll('text').attr('fill', 'var(--ink-faint)');

            const line = d3.line()
              .x(d => x(d.day))
              .y(d => y(d.value))
              .curve(d3.curveMonotoneX);

            svg.append('path')
              .datum(weeklyData)
              .attr('fill', 'none')
              .attr('stroke', 'var(--indigo)')
              .attr('stroke-width', 3)
              .attr('d', line);

            svg.selectAll('.dot')
              .data(weeklyData)
              .enter().append('circle')
              .attr('cx', d => x(d.day))
              .attr('cy', d => y(d.value))
              .attr('r', 4)
              .attr('fill', 'var(--indigo)')
              .attr('stroke', 'var(--paper)')
              .attr('stroke-width', 2);
        }

        setTimeout(window.renderChart, 500);
        window.addEventListener('resize', window.renderChart);
        
        window.updateWeeklyData = function(newValue) {
            const today = new Date().toLocaleDateString('en-US', {weekday: 'short'});
            let found = weeklyData.find(d => d.day === today);
            if (found) {
                found.value += newValue;
            } else {
                weeklyData.push({ day: today, value: newValue });
                if (weeklyData.length > 7) weeklyData.shift();
            }
            localStorage.setItem('henkaWeeklyData', JSON.stringify(weeklyData));
            window.renderChart();
        }
"""
content = re.sub(tracker_vars_pattern, tracker_vars_new, content)

with open("index.html", "w") as f:
    f.write(content)
print("Done variables")
