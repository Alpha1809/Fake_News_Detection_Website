/**
 * Custom Chart.js extensions for the Fake News Detector
 * Implements a gauge chart type for confidence visualization
 */

// Register the gauge chart with Chart.js if it's loaded
if (typeof Chart !== 'undefined') {
    
    // Define a new chart type: gauge
    Chart.defaults.gauge = {
        aspectRatio: 1.5,
        rotation: -Math.PI / 2,
        circumference: Math.PI,
        animation: {
            animateRotate: true,
            animateScale: true
        },
        cutout: '75%',
        plugins: {
            legend: {
                display: false
            },
            tooltip: {
                enabled: false
            }
        }
    };
    
    // Extend Chart.js with the gauge controller
    class GaugeController extends Chart.controllers.doughnut {
        draw() {
            super.draw();
            
            const ctx = this.chart.ctx;
            const chartArea = this.chart.chartArea;
            
            // Only draw value text if we have a single dataset and value
            if (this.chart.data.datasets.length === 1) {
                const dataset = this.chart.data.datasets[0];
                const value = dataset.value || 0;
                const min = dataset.minValue || 0;
                const max = dataset.maxValue || 1;
                
                // Normalize the value between 0 and 1
                const normalizedValue = (value - min) / (max - min);
                
                // Get display text
                const displayText = this.chart.options.valueLabel && 
                                   this.chart.options.valueLabel.formatter ? 
                                   this.chart.options.valueLabel.formatter(value) : 
                                   `${(value * 100).toFixed(1)}%`;
                
                // Draw the value text
                const centerX = (chartArea.left + chartArea.right) / 2;
                const centerY = (chartArea.top + chartArea.bottom) / 2;
                
                ctx.save();
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.font = '24px Arial, sans-serif';
                ctx.fillStyle = '#333';
                ctx.fillText(displayText, centerX, centerY);
                ctx.restore();
                
                // Add label text if exists
                if (this.chart.options.valueLabel && this.chart.options.valueLabel.label) {
                    ctx.save();
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';
                    ctx.font = '16px Arial, sans-serif';
                    ctx.fillStyle = '#777';
                    ctx.fillText(this.chart.options.valueLabel.label, centerX, centerY + 30);
                    ctx.restore();
                }
            }
        }
    }
    
    // Register the new chart type
    Chart.register({
        id: 'gauge',
        controller: GaugeController,
    });
    
    // Create a method to update gauge charts easily
    Chart.prototype.updateGauge = function(value) {
        if (this.config.type === 'gauge' && this.data.datasets.length > 0) {
            this.data.datasets[0].value = value;
            this.update();
        }
    };
    
    // Fallback for browsers or Chart.js versions that don't support the gauge type
    if (!Chart.controllers.gauge) {
        console.warn('Gauge chart type not supported, falling back to doughnut');
        
        // Create a method to render gauge-like visuals with a doughnut chart
        window.createGaugeChart = function(ctx, options) {
            const value = options.value || 0;
            const min = options.minValue || 0;
            const max = options.maxValue || 1;
            
            // Normalize value 
            const normalizedValue = (value - min) / (max - min);
            
            return new Chart(ctx, {
                type: 'doughnut',
                data: {
                    datasets: [{
                        data: [normalizedValue, 1 - normalizedValue],
                        backgroundColor: [
                            options.color || '#0d6efd',
                            'rgba(200, 200, 200, 0.2)'
                        ],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    cutout: '75%',
                    rotation: -90,
                    circumference: 180,
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            enabled: false
                        }
                    }
                }
            });
        };
    }
}
