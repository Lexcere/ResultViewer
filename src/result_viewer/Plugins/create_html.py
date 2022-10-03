import tempfile
import configparser as ConfigParser
import os
import random
import string
import re

GREEN = "#99ee99"
RED = "#ff6666"
YELLOW = "#fed84f"


class ResultObject(object):
    def __init__(self):
        self.title = ""
        self.time = ""
        self.details = []
        self.font_color = "black"
        self.section = False


class TC_result_HTML():
    def __init__(self,):
        self.tmp_path = tempfile.mkdtemp()

    def create_file(self, tc_raw_result_path=r""):
        # Get the value in txt file
        Config = ConfigParser.ConfigParser()
        Config.read(tc_raw_result_path)
        self.tc_raw_result_path = tc_raw_result_path
        log = Config.get(section="ACTUAL RESULTS", option="log")
        log = log.split("\n")
        # Get Test Case Info
        self.tc_ID = Config.get(section="GENERIC",     option="test case number")
        self.tc_vers = Config.get(section="GENERIC",     option="test case version")
        self.tc_Desc = Config.get(section="GENERIC",     option="test case description")
        self.req_ID = Config.get(section="GENERIC",     option="requirement cover")
        self.req_ID = self.req_ID.lstrip()
        self.req_ID = self.req_ID.replace("\n", "<br>")
        self.measurement_file = Config.get(section="GENERIC",     option="measurement file/s")
        self.measurement_file = self.measurement_file.lstrip()
        self.measurement_file = self.measurement_file.split("\n")
        self.tc_date = Config.get(section="GENERIC",     option="test execution date")
        self.tc_sw = Config.get(section="ENVIRONMENT", option="sw number")
        self.tc_rev = Config.get(section="ENVIRONMENT", option="sw revision")
        self.tc_hil = Config.get(section="ENVIRONMENT", option="hil model")
        self.tc_a2lM = Config.get(section="ENVIRONMENT", option="a2l master")
        self.tc_a2lS = Config.get(section="ENVIRONMENT", option="a2l slave")
        self.tc_cdd = Config.get(section="ENVIRONMENT", option="cdd")
        self.tc_can1 = Config.get(section="ENVIRONMENT", option="can1 protocol")
        self.tc_can2 = Config.get(section="ENVIRONMENT", option="can2 protocol")
        self.tc_eng = Config.get(section="ENVIRONMENT", option="engine variant")

        # create randon name for file
        self.name = ""
        for i in range(0, 10, 1):
            self.name += random.choice(string.ascii_letters)

        # create the file
        self.pre_content = []
        self._open()
        for line in log:
            self._body(line)

        for obj in self.pre_content:
            if obj.title.find("*********** ") >= 0:
                message = obj.title.replace("*", "")
                self.f.write('<div class=tcsection><b>{0}</b></div>\n'.format(message))
            # Normal Results
            else:
                self.f.write("<button class='accordion_line'><font color = '{1}'>{0}</font></button>\n".format(obj.title, obj.font_color))
                self.f.write('<div class="panel_line">{0}<br>\n'.format(obj.time))
                for detail in obj.details:
                    self.f.write('{0}<br>'.format(detail))
                self.f.write('</div>\n')

        self._close()
        self.f = ""
        return self.tmp_path + r"\\" + self.name + ".html"

    def _open(self):
        self.f = open(self.tmp_path + r"\\" + self.name + ".html", "w")
        self.f.write('<!DOCTYPEhtml>\n')
        # Create HTML StyleSheet
        self.f.write('<style media="screen" type="text/css">\n')
        self.f.write('body {\n')
        self.f.write('    width: 100%;\n')
        self.f.write('    padding-left: 0em;\n')
        self.f.write('    padding-right: 0em;\n')
        self.f.write('    font-family: Segoe UI, Arial, sans-serif;\n')
        self.f.write('    color: black}\n')

        self.f.write('.instruction {\n')
        self.f.write('	  margin-left: 4em;\n')
        self.f.write('    margin-top: 0em;\n')
        self.f.write('	  margin-bottom: 0em;\n')
        self.f.write('    font-family: Segoe UI, Arial, sans-serif;\n')
        self.f.write('    font-size: 12px;\n')
        self.f.write('}\n')

        self.f.write('.header{\n')
        self.f.write('    position: fixed;\n')
        self.f.write('    margin-top: 0;\n')
        self.f.write('    padding-top: 0;\n')
        self.f.write('    top: 0;\n')
        self.f.write('    height: 50px;\n')
        self.f.write('    width: 100%;\n')
        self.f.write('    background: White;\n')
        self.f.write('}\n')

        self.f.write('.accordion {\n')
        self.f.write('  background-color: white;\n')
        self.f.write('  color: #444;\n')
        self.f.write('  cursor: pointer;\n')
        self.f.write('  padding: 18px;\n')
        self.f.write('  width: 100%;\n')
        self.f.write('  border: none;\n')
        self.f.write('  text-align: left;\n')
        self.f.write('  outline: none;\n')
        self.f.write('  font-size: 15px;\n')
        self.f.write('  transition: 0.4s;\n')
        self.f.write('}\n')
        self.f.write('.active, .accordion:hover {\n')
        self.f.write('    background-color: #eee;\n')
        self.f.write('    border: 1px solid #ccc;\n')
        self.f.write('}\n')

        self.f.write('.panel {\n')
        self.f.write('  padding: 0 18px;\n')
        self.f.write('  display: none;\n')
        self.f.write('  background-color: white;\n')
        self.f.write('  overflow: hidden;\n')
        self.f.write('}\n')

        self.f.write('.accordion_line {\n')
        self.f.write('	margin-left: 4em;\n')
        self.f.write('  background-color: white;\n')
        self.f.write('  color: black;\n')
        self.f.write('  cursor: pointer;\n')
        self.f.write('  padding: 0px;\n')
        self.f.write('  width: 100%;\n')
        self.f.write('  border: none;\n')
        self.f.write('  text-align: left;\n')
        self.f.write('  outline: none;\n')
        self.f.write('  font-size: 12px;\n')
        self.f.write('  font-family: Segoe UI, Arial, sans-serif;\n')
        self.f.write('}\n')

        self.f.write('.accordion_line:hover {\n')
        self.f.write('    background-color: #eee;\n')
        self.f.write('    border: 1px solid #ccc;\n')
        self.f.write('}\n')

        self.f.write('.active, .accordion_line:hover {\n')
        self.f.write('    background-color: #eee;\n')
        self.f.write('}\n')

        self.f.write('.panel_line {\n')
        self.f.write('  padding: 0 18px;\n')
        self.f.write('	margin-left: 4em;\n')
        self.f.write('  display: none;\n')
        self.f.write('  background-color: white;\n')
        self.f.write('  font-size: 12px;\n')
        self.f.write('  overflow: hidden;\n')
        self.f.write('  font-family: Segoe UI, Arial, sans-serif;\n')
        self.f.write('}\n')

        self.f.write('table {\n')
        self.f.write('font-family: Segoe UI, Arial, sans-serif;\n')
        self.f.write('border-collapse: collapse;\n')
        self.f.write('width: 100%;\n')
        self.f.write('font-size: 12px;\n')
        self.f.write('}\n')
        self.f.write('td, th {\n')
        self.f.write('border: 1px solid  #dddddd;\n')
        self.f.write('text-align: left;\n')
        self.f.write('padding: 8px;\n')
        self.f.write('}\n')

        self.f.write('.tcsection {\n')
        self.f.write('    margin-top: 10px;\n')
        self.f.write('    margin-left: 45px;\n')
        self.f.write('    position: sticky;\n')
        self.f.write('    background: white;\n')
        self.f.write('    top: 0;\n')
        self.f.write('}\n')

        self.f.write('.line {\n')
        self.f.write('    width: 100%;\n')
        self.f.write('    display:inline-block;\n')
        self.f.write('    float: left;\n')
        self.f.write('    \n')
        self.f.write('}\n')
        self.f.write('.line:hover {\n')
        self.f.write('    background-color: #eee;\n')
        self.f.write('    border: 1px solid #ccc;\n')
        self.f.write('    position: absolute;\n')
        self.f.write('}\n')

        self.f.write('</style>\n')

        # End of HEAD Section
        self.f.write('</head>\n')

        self.f.write('<html>\n')
        self.f.write('<body>\n')

        self.f.write('<button class="accordion">' + self.tc_ID + '&emsp;&emsp;' + self.tc_Desc + '</button>\n')
        self.f.write('<div class="panel">\n')
        self.f.write('<table>\n')
        self.f.write('<tr>\n')
        self.f.write('<th>TestCase ID</th>\n')
        self.f.write('<td>' + self.tc_ID + '</td>\n')
        self.f.write('</tr>\n')
        self.f.write('<tr>\n')
        self.f.write('<th>Description</th>\n')
        self.f.write('<td>' + self.tc_Desc + '</td>\n')
        self.f.write('</tr>\n')
        self.f.write('<tr>\n')
        self.f.write('<th>Test Date</th>\n')
        self.f.write('<td>' + self.tc_date + '</td>\n')
        self.f.write('</tr>\n')
        self.f.write('<tr>\n')
        self.f.write('<th>Requirement(s)</th>\n')
        self.f.write('<td>' + self.req_ID + '</td>\n')
        self.f.write('</tr>\n')
        self.f.write('<tr>\n')
        self.f.write('<th>Measurement file/s</th>\n')
        self.f.write('<td>')
        file_path = os.path.dirname(self.tc_raw_result_path)
        for meas in self.measurement_file:
            self.f.write(r'<a href="{1}\{0}" target="_blank">{0}</a><br>\n'.format(meas, file_path))
        self.f.write('</td>\n')
        self.f.write('</tr>\n')
        self.f.write('<tr>\n')
        self.f.write('<th>Software</th>\n')
        self.f.write('<td>' + self.tc_sw + '</td>\n')
        self.f.write('</tr>\n')
        self.f.write('<tr>\n')
        self.f.write('<th>Revision</th>\n')
        self.f.write('<td>' + self.tc_rev + '</td>\n')
        self.f.write('</tr>\n')
        self.f.write('<tr>\n')
        self.f.write('<th>HIL Model</th>\n')
        self.f.write('<td>' + self.tc_hil + '</td>\n')
        self.f.write('</tr>\n')
        self.f.write('<tr>\n')
        self.f.write('<th>A2L Master</th>\n')
        self.f.write('<td>' + self.tc_a2lM + '</td>\n')
        self.f.write('</tr>\n')
        self.f.write('<tr>\n')
        self.f.write('<th>A2L Slave</th>\n')
        self.f.write('<td>' + self.tc_a2lS + '</td>\n')
        self.f.write('</tr>\n')
        self.f.write('<tr>\n')
        self.f.write('<th>CDD Master</th>\n')
        self.f.write('<td>' + self.tc_cdd + '</td>\n')
        self.f.write('</tr>\n')
        self.f.write('<tr>\n')
        self.f.write('<th>CAN1 Protocol</th>\n')
        self.f.write('<td>' + self.tc_can1 + '</td>\n')
        self.f.write('</tr>\n')
        self.f.write('<tr>\n')
        self.f.write('<th>CAN2 Protocol</th>\n')
        self.f.write('<td>' + self.tc_can2 + '</td>\n')
        self.f.write('</tr>\n')
        self.f.write('<tr>\n')
        self.f.write('<th>Engine Type</th>\n')
        self.f.write('<td>' + self.tc_eng + '</td>\n')
        self.f.write('</tr>\n')

        self.f.write('</table>\n')
        self.f.write('</div>\n')

        self.f.write('<br>\n')

        self.f.write("<input type='button' id='toggle_button' value='Expand all' />\n")
        self.f.write("<br>\n")

    def _body(self, text_to_write=""):
        if re.search(r'\d\d:\d\d:\d\d', text_to_write) is not None:
            self.temp_obj = ResultObject()
            index = re.search(r"\d\d:\d\d:\d\d.\d\d\d", text_to_write).end()
            time = text_to_write[:index]
            title = text_to_write[index:]
            detail = text_to_write.split("\t\t\t")[2:]
            self.temp_obj.title = title
            self.temp_obj.time = time
            if detail != []:
                for d in detail:
                    self.temp_obj.details.append(d)
            if self.temp_obj.title.find("NOT OK") >= 0 or self.temp_obj.title.find("TestHandler") >= 0:
                self.temp_obj.font_color = RED
            self.pre_content.append(self.temp_obj)
        else:
            self.temp_obj.details.append(text_to_write)

    def _close(self):
        # CREATE SCRIPT SECTION
        # self.f.write("<script src='http://ajax.aspnetcdn.com/ajax/jQuery/jquery-3.2.1.js'></script>\n")
        self.f.write(r"<script src='C:\CAD\Workspace\HILSimulator\HIL_Tools\TestCase_RawResult_Manager\.data\jquery-3.2.1.js.download'></script>\n")
        self.f.write('<script type="text/javascript">\n')

        self.f.write("$(document).ready(function(){\n")
        self.f.write(" $('#toggle_button').click(function(){\n")
        self.f.write("   //$('#txt1').val('Button clicked');\n")
        self.f.write("   \n")
        self.f.write("   var panel = document.getElementsByClassName('panel_line');\n")
        self.f.write("   var i;\n")
        self.f.write("   for (i = 0; i < panel.length; i++) {\n")
        self.f.write("    if (panel[i].style.display === 'block') {\n")
        self.f.write("     panel[i].style.display = 'none';\n")
        self.f.write("     $('#toggle_button').val('Expand all');\n")
        self.f.write("    } else {\n")
        self.f.write("      panel[i].style.display = 'block';\n")
        self.f.write("      $('#toggle_button').val('Collapse all');\n")
        self.f.write("    }\n")
        self.f.write("   }\n")
        self.f.write("   \n")
        self.f.write(" });\n")
        self.f.write("});\n")

        self.f.write('var acc = document.getElementsByClassName("accordion");\n')
        self.f.write('var i;\n')
        self.f.write('for (i = 0; i < acc.length; i++) {\n')
        self.f.write('  acc[i].addEventListener("click", function() {\n')
        self.f.write('    this.classList.toggle("active");\n')
        self.f.write('    var panel = this.nextElementSibling;\n')
        self.f.write('    if (panel.style.display === "block") {\n')
        self.f.write('      panel.style.display = "none";\n')
        self.f.write('    } else {\n')
        self.f.write('      panel.style.display = "block";\n')
        self.f.write('    }\n')
        self.f.write('  });\n')
        self.f.write('}\n')

        self.f.write('var acc = document.getElementsByClassName("accordion_line");\n')
        self.f.write('var i;\n')
        self.f.write('for (i = 0; i < acc.length; i++) {\n')
        self.f.write('  acc[i].addEventListener("click", function() {\n')
        self.f.write('    this.classList.toggle("active");\n')
        self.f.write('    var panel = this.nextElementSibling;\n')
        self.f.write('    if (panel.style.display === "block") {\n')
        self.f.write('      panel.style.display = "none";\n')
        self.f.write('    } else {\n')
        self.f.write('      panel.style.display = "block";\n')
        self.f.write('    }\n')
        self.f.write('  });\n')
        self.f.write('}\n')
        self.f.write('</script>\n')
        self.f.write('</body>\n')
        self.f.write('</html>\n')

        self.f.close()
