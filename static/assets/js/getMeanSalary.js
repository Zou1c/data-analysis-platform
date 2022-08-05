 $.ajax({
                //待修改 根据后端接口而定

                url: '/getjobsalarybytype',
                method: 'post',
                data: {

                },
                dataType: "json",
                success: function (data) {
                    labels = []
                    values = []
                    for(i=0;i<data.length;i++){
                        labels[i] = data[i].jobType
                        values[i] = data[i].jobsavg
                    }

                    var chartDom = document.getElementById('meanSalaryMap');
                    var myChart = echarts.init(chartDom);
                    var option;

                    option = {
                      xAxis: {
                        type: 'category',
                        data: labels
                      },
                      yAxis: {
                        type: 'value'
                      },
                      series: [
                        {
                          data: values,
                          type: 'bar'
                        }
                      ]
                    };

                    option && myChart.setOption(option);

                },
                error: function (xhr) {
                }
            })