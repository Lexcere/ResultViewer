import configparser
import os
import re
import time
import datetime
import csv
import collections

GREEN = "#99ee99"
RED = "#ff6666"
YELLOW = "#fed84f"
GREY = "#dddddd"
DARK_GREY_CSS = "#ccc"


class ReportHTML:
    def __init__(self, output_dir, files=None):
        # check the directory exist
        if not os.path.isdir(output_dir):
            print("Folder choosen does not exist")
            return -1

        self.files = files
        self.Config = configparser.RawConfigParser()
        self.save_directory = output_dir
        self.info_available = False
        self.other_restriction_available = False
        self.deviation_assesment_avaliable = False

        today = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
        self.ReportFileName = r"{0}\\TestSummaryReport_{1}.html".format(output_dir, today)

        # create file
        self.report = open(self.ReportFileName, "w")

        self.ReadInfoFile()
        self.ReadOtherRestrictionFile()
        self.ReadDeviationAssesmentFile()

        # populate report header
        self.report.write('<!DOCTYPE html>\n')

        self.report.write('<html>\n')
        self.report.write('<head>\n')
        self.report.write('<meta name="viewport" content = "width=device-width, initial-scale=1">\n')

        # Create HTML StyleSheet
        self.WriteStyleSheet()

        # End of HEAD Section
        self.report.write('</head>\n')

        # Start of body section
        self.report.write('<body>\n')

        self.report.write('<div class="tab">\n')
        self.report.write("""<button class="tablinks" onclick="showContent(event, 'Summary')">Summary</button>\n""")
        self.report.write("""<button class="tablinks" onclick="showContent(event, 'Result')">Result</button>\n""")
        self.report.write("""<button class="tablinks" onclick="showContent(event, 'Traceability')">Traceability</button>\n""")
        self.report.write("""<button class="tablinks" onclick="showContent(event, 'Deviation')">Deviation</button>\n""")
        self.report.write("""<button class="tablinks" onclick="showContent(event, 'Details')">Details</button>\n""")
        self.report.write('</div>\n')

        self.report.write('<div id="Summary" class="tabcontent" style="display:block">\n')  # style is added to make the tab active at beginnin
        self.CreateSummary()
        self.report.write('</div>\n')

        self.report.write('<div id="Result" class="tabcontent">\n')
        self.CreateResultTable()
        self.report.write('</div>\n')

        self.report.write('<div id="Traceability" class="tabcontent">\n')
        self.CreatMatrixtTable()
        self.report.write('</div>\n')

        self.report.write('<div id="Deviation" class="tabcontent">\n')
        self.CreateDeviationTable()
        self.report.write('</div>\n')

        self.report.write('<div id="Details" class="tabcontent">\n')
        self.CreateDetailsTable()
        self.report.write('</div>\n')

        # Start script section
        self.report.write('<script>\n')

        self.report.write('function showContent(evt, content) {\n')
        self.report.write('		  var i, tabcontent, tablinks;\n')
        self.report.write('		  tabcontent = document.getElementsByClassName("tabcontent");\n')
        self.report.write('		  for (i = 0; i < tabcontent.length; i++) {\n')
        self.report.write('			tabcontent[i].style.display = "none";\n')
        self.report.write('		  }\n')
        self.report.write('		  tablinks = document.getElementsByClassName("tablinks");\n')
        self.report.write('		  for (i = 0; i < tablinks.length; i++) {\n')
        self.report.write('			tablinks[i].className = tablinks[i].className.replace(" active", "");\n')
        self.report.write('		  }\n')
        self.report.write('		  document.getElementById(content).style.display = "block";\n')
        self.report.write('		  evt.currentTarget.className += " active";\n')
        self.report.write('		}\n')

        self.report.write('var acc = document.getElementsByClassName("accordion");\n')
        self.report.write('var i;\n')
        self.report.write('for (i = 0; i < acc.length; i++) {\n')
        self.report.write('  acc[i].addEventListener("click", function() {\n')
        self.report.write('    this.classList.toggle("active");\n')
        self.report.write('    var panel = this.nextElementSibling;\n')
        self.report.write('    if (panel.style.display === "block") {\n')
        self.report.write('      panel.style.display = "none";\n')
        self.report.write('    } else {\n')
        self.report.write('      panel.style.display = "block";\n')
        self.report.write('    }\n')
        self.report.write('  });\n')
        self.report.write('}\n')

        self.report.write('</script>\n')
        self.report.write('</body>\n')
        self.report.write('</html>\n')

        # close file
        self.report.close()

    def ReadInfoFile(self):
        info_path = ""

        for dirpath, dirs, files in os.walk(self.save_directory):
            for f in files:  # for each file in the folder
                if f.find("info.csv") >= 0:
                    info_path = r"{0}\{1}".format(dirpath, f)
                    self.info_available = True
                    break
            if info_path != "":
                break

        if self.info_available:
            csv_file = open(info_path, "r")
            reader = csv.reader(csv_file, delimiter=";")
            for row in reader:
                if row[0] == "Maturity":
                    self.maturity = row[1]
                elif row[0] == "Project":
                    self.project = row[1]

    def ReadOtherRestrictionFile(self):
        other_restriction_path = ""

        for dirpath, dirs, files in os.walk(self.save_directory):
            for f in files:  # for each file in the folder
                if f.find("other_restriction.csv") >= 0:
                    other_restriction_path = r"{0}\{1}".format(dirpath, f)
                    self.other_restriction_available = True
                    break
            if other_restriction_path != "":
                break

        if self.other_restriction_available:
            self.other_restriction = []

            csv_file = open(other_restriction_path, "r")
            reader = csv.reader(csv_file, delimiter=";")
            next(reader)
            for row in reader:
                self.other_restriction.append(row[0])

    def ReadDeviationAssesmentFile(self):
        deviation_assesment_path = ""

        for dirpath, dirs, files in os.walk(self.save_directory):
            for f in files:  # for each file in the folder
                if f.find("deviation_assesment") >= 0:
                    deviation_assesment_path = r"{0}\{1}".format(dirpath, f)
                    self.deviation_assesment_avaliable = True
                    break
            if deviation_assesment_path != "":
                break

        if self.deviation_assesment_avaliable:
            self.deviation_assesment = {}

            csv_file = open(deviation_assesment_path, "r")
            reader = csv.reader(csv_file, delimiter=";")
            next(reader)
            for row in reader:
                self.deviation_assesment[row[0]] = {}
                tmp = row[1].upper()
                if tmp == "YES" or tmp == "NO":
                    self.deviation_assesment[row[0]]["blocking"] = tmp
                else:
                    raise AssertionError("'Blocking' string from deviation file is not correct")
                tmp = row[2]
                tmp = tmp.replace("\n", "<br>")
                self.deviation_assesment[row[0]]["comment"] = tmp

    def WriteStyleSheet(self):
        self.report.write('<style>\n')

        self.report.write('body {\n')
        self.report.write('width: 100 %;\n')
        self.report.write('padding-left: 0em;\n')
        self.report.write('padding-right: 0em;\n')
        self.report.write('font-family: Segoe UI, Arial, sans-serif;\n')
        self.report.write('color: black\n')
        self.report.write('}\n')

        self.report.write('.instruction {\n')
        self.report.write('    margin-left: 4em;\n')
        self.report.write('    margin-top: 0em;\n')
        self.report.write('    margin-bottom: 0em;\n')
        self.report.write('    font-family: Segoe UI, Arial, sans-serif;\n')
        self.report.write('    font-size: 12px;\n')
        self.report.write('}\n')

        self.report.write('table {\n')
        self.report.write('    font-family: Segoe UI, Arial, sans-serif;\n')
        self.report.write('    border-collapse: collapse;\n')
        self.report.write('    width: 100%;\n')
        self.report.write('    font-size: 12px;\n')
        self.report.write('}\n')

        self.report.write('td, th {\n')
        self.report.write('border: 1px solid  #dddddd;\n')
        self.report.write('text-align: left;\n')
        self.report.write('padding: 8px;\n')
        self.report.write('}\n')

        self.report.write('.tab {\n')
        self.report.write('position: sticky;;\n')
        self.report.write('top: 0;\n')
        self.report.write('overflow: hidden;\n')
        self.report.write('border: 1px solid  #ccc;\n')
        self.report.write('background-color:  #1f4e9a;\n')
        self.report.write('}\n')

        self.report.write('.tab button {\n')
        self.report.write('background-color: #1f4e9a;\n')
        self.report.write('float: left;\n')
        self.report.write('border: none;\n')
        self.report.write('outline: none;\n')
        self.report.write('cursor: pointer;\n')
        self.report.write('padding: 14px 16px;\n')
        self.report.write('transition: 0.3s;\n')
        self.report.write('font-size: 17px;\n')
        self.report.write('color: white;\n')
        self.report.write('}\n')

        self.report.write('.tab button:hover {\n')
        self.report.write('background-color:  #4c72ae;\n')
        self.report.write('}\n')

        self.report.write('.tab button.active {\n')
        self.report.write('background-color:  #4c72ae;\n')
        self.report.write('}\n')

        self.report.write('.tabcontent {\n')
        self.report.write('display: None;\n')
        self.report.write('padding: 6px 12px;\n')
        self.report.write('border: 1px solid  #ccc;\n')
        self.report.write('border-top: none;\n')
        self.report.write('}\n')

        self.report.write('.header_table_cover {\n')
        self.report.write('    width:auto;\n')
        self.report.write('    margin:auto;\n')
        self.report.write('    border-collapse: collapse;\n')
        self.report.write('    font-size: 20px;\n')
        self.report.write('}\n')

        self.report.write('.header_table_cover  th{\n')
        self.report.write('    width:50%;\n')
        self.report.write('    text-align:right;\n')
        self.report.write('    padding: 5px;\n')
        self.report.write('}\n')

        self.report.write('.header_table_cover  td{\n')
        self.report.write('    text-align:center;\n')
        self.report.write('    padding: 5px;\n')
        self.report.write('}\n')

        self.report.write('.description_table_cover {\n')
        self.report.write('    width:15%;\n')
        self.report.write('    margin:auto;\n')
        self.report.write('    border-collapse: collapse;\n')
        self.report.write('}\n')

        self.report.write('.description_table_cover  th{\n')
        self.report.write('    width:50%;\n')
        self.report.write('    text-align:right;\n')
        self.report.write('    padding: 5px;\n')
        self.report.write('}\n')

        self.report.write('.description_table_cover  td{\n')
        self.report.write('    text-align:center;\n')
        self.report.write('    padding: 5px;\n')
        self.report.write('}\n')

        self.report.write('/* header_table_statistic */\n')
        self.report.write('.header_table_statistic {\n')
        self.report.write('}\n')
        self.report.write('.header_table_statistic  th{\n')
        self.report.write('    text-align:center;\n')
        self.report.write('    border: 1px solid #ccc;;\n')
        self.report.write('}\n')
        self.report.write('.header_table_statistic  td{\n')
        self.report.write('    text-align:center;\n')
        self.report.write('    border: 1px solid #ccc;;\n')
        self.report.write('}\n')

        self.report.write('.div1{\n')
        self.report.write('    display: inline-block\n')
        self.report.write('}\n')

        self.report.write('.accordion {\n')
        self.report.write('  background-color: #eee;\n')
        self.report.write('  color: #444;\n')
        self.report.write('  cursor: pointer;\n')
        self.report.write('  padding: 18px;\n')
        self.report.write('  width: 100%;\n')
        self.report.write('  border: none;\n')
        self.report.write('  text-align: left;\n')
        self.report.write('  outline: none;\n')
        self.report.write('  font-size: 15px;\n')
        self.report.write('  transition: 0.4s;\n')
        self.report.write('}\n')

        self.report.write('.active, .accordion:hover {\n')
        self.report.write('  background-color: #ccc; \n')
        self.report.write('}\n')

        self.report.write('.panel {\n')
        self.report.write('  padding: 0 18px;\n')
        self.report.write('  display: none;\n')
        self.report.write('  background-color: white;\n')
        self.report.write('  overflow: hidden;\n')
        self.report.write('}\n')

        self.report.write('.center {\n')
        self.report.write('  margin: auto;\n')
        self.report.write('  width: 60%;\n')
        self.report.write('  padding: 1px;\n')
        self.report.write('  text-align: center;\n')
        self.report.write('}\n')

        self.report.write('hr.new1 {\n')
        self.report.write('  border-top: 1px solid Gainsboro;\n')
        self.report.write('}\n')

        self.report.write('</style>\n')

    def CreateSummary(self):
        total_tc = 0
        ok_tc = 0
        nok_tc = 0
        not_tested_tc = 0

        safety_total_tc = 0
        safety_ok_tc = 0
        safety_nok_tc = 0
        safety_not_tested_tc = 0

        ramd_total_tc = 0
        ramd_ok_tc = 0
        ramd_nok_tc = 0
        ramd_not_tested_tc = 0

        defect_counter = []
        sw_number_list = []
        sw_revision_list = []
        sw = ""
        revision = ""

        for test_result in self.files:
            self.Config = configparser.RawConfigParser()
            self.Config.read(test_result)
            total_tc += 1

            tmp_result = self.Config.get(section="GENERIC", option="result")
            tmp_tc_id = self.Config.get(section="GENERIC", option="test case number")
            tmp_incident_no = self.Config.get(section="GENERIC", option="incident number")
            tmp_sw_number = self.Config.get(section="ENVIRONMENT", option="sw number")
            tmp_sw_revision = self.Config.get(section="ENVIRONMENT", option="sw revision")

            if tmp_result == "OK":
                ok_tc += 1
            elif tmp_result == "NOT OK":
                nok_tc += 1
            elif tmp_result == "NOT TESTED":
                not_tested_tc += 1

            if tmp_tc_id.find("Safety") >= 0:
                safety_total_tc += 1
                if tmp_result == "OK":
                    safety_ok_tc += 1
                elif tmp_result == "NOT OK":
                    safety_nok_tc += 1
                elif tmp_result == "NOT TESTED":
                    safety_not_tested_tc += 1

            if tmp_tc_id.find("RAMD") >= 0:
                ramd_total_tc += 1
                if tmp_result == "OK":
                    ramd_ok_tc += 1
                elif tmp_result == "NOT OK":
                    ramd_nok_tc += 1
                elif tmp_result == "NOT TESTED":
                    ramd_not_tested_tc += 1

            # count defect
            if tmp_incident_no != "":
                if tmp_incident_no not in defect_counter:
                    defect_counter.append(tmp_incident_no)

            if tmp_sw_number not in sw_number_list:
                sw_number_list.append(tmp_sw_number)

            if tmp_sw_revision not in sw_revision_list:
                sw_revision_list.append(tmp_sw_revision)

        if len(set(sw_number_list)) == 1:
            sw = sw_number_list[0]
        else:
            for i in sw_number_list:
                if sw == "":
                    sw = i
                else:
                    sw = "{0} ; {1}".format(sw, i)

        if len(set(sw_revision_list)) == 1:
            revision = sw_revision_list[0]
        else:
            for i in sw_revision_list:
                if revision == "":
                    revision = i
                else:
                    revision = "{0} ; {1}".format(revision, i)

        self.report.write('<br>\n')
        self.report.write('<br>\n')

        self.report.write('<table class="header_table_cover">\n')
        self.report.write('	<tr>\n')
        self.report.write('	<th>Software</th>\n')
        self.report.write('	<td nowrap>{0}</td>\n'.format(sw))
        self.report.write('	</tr>\n')
        self.report.write('	<tr>\n')
        self.report.write('	<th>Revision</th>\n')
        self.report.write('	<td nowrap>{0}</td>\n'.format(revision))
        self.report.write('	</tr>\n')
        if self.info_available:
            self.report.write('	<tr>\n')
            self.report.write('	<th>Maturity</th>\n')
            self.report.write('	<td>{0}</td>\n'.format(self.maturity))
            self.report.write('	</tr>\n')
            self.report.write('	<tr>\n')
            self.report.write('	<th>Project</th>\n')
            self.report.write('	<td>{0}</td>\n'.format(self.project))
            self.report.write('	</tr>\n')
        else:
            self.report.write('	<tr>\n')
            self.report.write('	<th>Maturity</th>\n')
            self.report.write('	<td>(NA)</td>\n')
            self.report.write('	</tr>\n')
            self.report.write('	<tr>\n')
            self.report.write('	<th>Project</th>\n')
            self.report.write('	<td>(NA)</td>\n')
            self.report.write('	</tr>\n')

        self.report.write('	<tr>\n')
        self.report.write('	<th>Release status</th>\n')

        if self.deviation_assesment_avaliable:
            blocking = False
            blocking_counter = 0
            for k in self.deviation_assesment.keys():
                if self.deviation_assesment[k]["blocking"] == "YES":
                    blocking = True
                    blocking_counter += 1
            if blocking:
                self.report.write('	<td><font color="red">NOT RELEASED</font></td>\n')
            else:
                self.report.write('	<td><font color="green">RELEASED</font></td>\n')
        else:
            self.report.write('	<td>DRAFT FOR REVIEW</td>\n')
        self.report.write('	</tr>\n')
        self.report.write('</table>\n')

        self.report.write('<br>\n')
        self.report.write('<hr  class="new1">\n')
        self.report.write('<br>\n')

        self.report.write('<div class="center">\n')
        self.report.write('<div class="div1">\n')
        self.report.write('<table class="header_table_statistic">\n')
        self.report.write('	<tr>\n')
        self.report.write(f'	<th bgcolor="{GREY}"> </th>\n')
        self.report.write(f'	<th bgcolor="{GREY}">Total</th>\n')
        self.report.write(f'	<th bgcolor="{GREY}">Pass</th>\n')
        self.report.write(f'	<th bgcolor="{GREY}">Fail</th>\n')
        self.report.write(f'	<th bgcolor="{GREY}">Skipped</th>\n')
        self.report.write('	</tr>\n')
        self.report.write('	<tr>\n')
        self.report.write('	<th>All Tests</th>\n')
        self.report.write(f'	<td>{total_tc}</td>\n')
        self.report.write(f'	<td>{ok_tc}</td>\n')
        self.report.write(f'	<td>{nok_tc}</td>\n')
        self.report.write(f'	<td>{not_tested_tc}</td>\n')
        self.report.write('	</tr>\n')
        self.report.write('	<tr>\n')
        self.report.write('	<th>Safety</th>\n')
        self.report.write(f'	<td>{safety_total_tc}</td>\n')
        self.report.write(f'	<td>{safety_ok_tc}</td>\n')
        self.report.write(f'	<td>{safety_nok_tc}</td>\n')
        self.report.write(f'	<td>{safety_not_tested_tc}</td>\n')
        self.report.write('	</tr>\n')
        self.report.write('	<tr>\n')
        self.report.write('	<th>RAMD</th>\n')
        self.report.write(f'	<td>{ramd_total_tc}</td>\n')
        self.report.write(f'	<td>{ramd_ok_tc}</td>\n')
        self.report.write(f'	<td>{ramd_nok_tc}</td>\n')
        self.report.write(f'	<td>{ramd_not_tested_tc}</td>\n')
        self.report.write('	<tr>\n')
        self.report.write('</table>\n')
        self.report.write('</div>\n')
        self.report.write('</div>\n')

        self.report.write('<br>\n')
        self.report.write('<hr  class="new1">\n')
        self.report.write('<br>\n')

        self.report.write('<div class="center">\n')
        self.report.write('<font size="5">{0} Deviation(s)</font>\n'.format(len(defect_counter)))
        self.report.write('</div>\n')

        if self.deviation_assesment_avaliable:
            self.report.write('<br>\n')
            self.report.write('<div class="center">\n')
            self.report.write('<font size="3">{0} Blocking</font>\n'.format(blocking_counter))
            self.report.write('</div>\n')

        if self.other_restriction_available:
            self.report.write('<br>\n')
            self.report.write('<hr  class="new1">\n')
            self.report.write('<br>\n')
            self.report.write('<div class="center">\n')
            self.report.write('<font size="5">Release restriction</font>\n')
            self.report.write('<br>\n')
            self.report.write('<p style="text-align:justify">\n')
            for restriction in self.other_restriction:
                self.report.write('- {0}<br>\n'.format(restriction))
            self.report.write('</p>\n')
            self.report.write('</div>\n')
            self.report.write('<br>\n')
            self.report.write('<div class="center">\n')
            self.report.write('<p style="text-align:justify">\n')
            self.report.write('<font color="gray">These Comments are related to external test cases which are not performed as part of this test report. There may be no test cases or deviations shown in this report which cover these items.</font>\n')  # noqa
            self.report.write('</p>\n')
            self.report.write('</div>\n')

        self.report.write('<br>\n')
        self.report.write('<hr  class="new1">\n')
        self.report.write('<br>\n')
        self.report.write('<div class="center">\n')
        self.report.write('<font color="gray">This document contain only the results of test performed with different tools/environment.<br> The final decision of whether to release the SW is performed using the AC Report Approval Workflow in Sharepoint.</font>\n')  # noqa
        self.report.write('</div>\n')

        self.report.write('<br>\n')
        self.report.write('<br>\n')
        self.report.write('<table class="description_table_cover">\n')
        self.report.write('		  <tr>\n')
        self.report.write('			<td>Status</td>\n')
        self.report.write('			<td>Description</td>\n')
        self.report.write('		  </tr>\n')
        self.report.write('<tr>\n')
        self.report.write('<tr>\n')
        self.report.write('<td nowrap bgcolor="green">PASS</td>\n')
        self.report.write('<td nowrap>Test Case executed with expected results. No problems detected.</td>\n')
        self.report.write('</tr>\n')
        self.report.write('<tr>\n')
        self.report.write('<td nowrap bgcolor="red">FAIL</td>\n')
        self.report.write('<td nowrap>Test Case executed with unexpected results.<br>A description of the issue(s) can be found in the JIRA incident number linked to each test case.</td>\n')  # noqa
        self.report.write('</tr>\n')
        self.report.write('<tr>\n')
        self.report.write(f'<td nowrap bgcolor="{YELLOW}">SKIPPED</td>\n')
        self.report.write('<td nowrap>The test case is not required for this application or cannot be tested for technical reasons.<br>Unless specifically written in the release notes, no further tests or actions are required</td>\n')  # noqa
        self.report.write('</tr>\n')
        self.report.write('</table>\n')

        self.report.write('<br>\n')
        self.report.write('<br>\n')
        self.report.write('<br>\n')
        self.report.write('<br>\n')
        self.report.write('<font color="gray" size="1">Report generated on {0}</font>\n'.format(datetime.datetime.today().date()))

    def CreateResultTable(self):
        self.report.write('<table>\n')
        self.report.write('		  <tr>\n')
        self.report.write('			<th>TestCase</th>\n')
        self.report.write('			<th>Requirement</th>\n')
        self.report.write('			<th>Description</th>\n')
        self.report.write('			<th>Result</th>\n')
        self.report.write('			<th>Comment</th>\n')
        self.report.write('			<th>Incident No</th>\n')
        self.report.write('		  </tr>\n')

        for test_result in self.files:
            self.Config = configparser.RawConfigParser()
            self.Config.read(test_result)

            self.report.write('<tr>\n')
            self.report.write('<td>{0}</td>\n'.format(self.Config.get(section="GENERIC", option="test case number")))
            requirement = self.Config.get(section="GENERIC", option="requirement cover")
            requirement = requirement.lstrip()
            requirement = requirement.replace("\n", "<br>")
            self.report.write('<td>{0}</td>\n'.format(requirement))
            self.report.write('<td>{0}</td>\n'.format(self.Config.get(section="GENERIC", option="test case description")))
            if self.Config.get(section="GENERIC", option="result") == "OK":
                self.report.write(f'<td nowrap bgcolor="{GREEN}">PASS</td>\n')
            elif self.Config.get(section="GENERIC", option="result") == "NOT OK":
                self.report.write(f'<td nowrap bgcolor="{RED}">FAIL</td>\n')
            else:
                self.report.write('<td nowrap>{0}</td>\n'.format(self.Config.get(section="GENERIC", option="result")))
            self.report.write('<td>{0}</td>\n'.format(self.Config.get(section="GENERIC", option="comment")))
            self.report.write('<td nowrap><a href="https://jira.zdv.liebherr.i/browse/{0}" target="_blank">{0}</a></td>\n'.format(self.Config.get(section="GENERIC", option="incident number")))  # noqa
            self.report.write('</tr>\n')

        self.report.write('</table>\n')

    def CreatMatrixtTable(self):
        self.report.write('<table>\n')
        self.report.write('<tr>\n')
        self.report.write('<th>Requirement</th>\n')
        self.report.write('<th>TestCase</th>\n')
        self.report.write('<th>Pass ratio</th>\n')
        self.report.write('<th>Status</th>\n')
        self.report.write('<th>Comment</th>\n')
        self.report.write('</tr>\n')

        dictionary_of_requirement = {}
        dictionary_of_results = {}
        dictionary_of_comments = {}

        for test_result in self.files:
            self.Config = configparser.RawConfigParser()
            self.Config.read(test_result)

            tc_id = self.Config.get(section="GENERIC", option="test case number")
            requirement = self.Config.get(section="GENERIC", option="requirement cover")
            result = self.Config.get(section="GENERIC", option="result")
            comment = self.Config.get(section="GENERIC", option="comment")
            if requirement != "":
                # split in lines
                requirement = requirement.split("\n")
                # remove first void line
                requirement = requirement[1:]
                for r in requirement:
                    if r not in dictionary_of_requirement.keys():
                        dictionary_of_requirement[str(r)] = []
                        dictionary_of_results[str(r)] = []
                        dictionary_of_comments[str(r)] = []
                    dictionary_of_requirement[str(r)].append(tc_id)
                    dictionary_of_results[str(r)].append(result)
                    if comment not in dictionary_of_comments[str(r)] and comment != "":  # if comment no already in dictionary and not empty -> add it
                        dictionary_of_comments[str(r)].append(comment)

        # Start to write on table the data contained in the dictionary
        for i in dictionary_of_requirement.keys():
            self.report.write('<tr>\n')
            # Write the requirement
            self.report.write('<td>{0}</td>\n'.format(i))

            # write the Testcase/s
            value_to_write = ""
            for y in dictionary_of_requirement[i]:
                if value_to_write == "":
                    value_to_write = y
                else:
                    value_to_write = value_to_write + "<br>" + y
            self.report.write('<td>{0}</td>\n'.format(value_to_write))

            # Write the pass ration
            total_test = len(dictionary_of_results[i])
            ok = 0
            nok = 0
            not_tested = 0
            for unit_result in dictionary_of_results[i]:
                if unit_result == "OK":
                    ok += 1
                elif unit_result == "NOT OK":
                    nok += 1
                elif unit_result == "NOT TESTED":
                    not_tested += 1
            ok = (ok * 100) / total_test
            nok = (nok * 100) / total_test
            not_tested = (not_tested * 100) / total_test
            value_to_write = "PASS: " + str(ok) + "%<br>"
            value_to_write = value_to_write + "FAIL: " + str(nok) + "%<br>"
            value_to_write = value_to_write + "SKIPPED: " + str(not_tested) + "%"
            self.report.write('<td nowrap>{0}</td>\n'.format(value_to_write))

            # write the status
            if ok == 100:
                self.report.write(f'<td nowrap bgcolor="{GREEN}">PASS</td>\n')
            elif nok > 0:
                self.report.write(f'<td nowrap bgcolor="{RED}">FAIL</td>\n')
            elif not_tested == 100:
                self.report.write(f'<td nowrap bgcolor="{YELLOW}">SKIPPED</td>\n')
            elif not_tested > 0 and nok == 0 and ok > 0:
                self.report.write(f'<td nowrap bgcolor="{YELLOW}">PARTIAL</td>\n')

            # write the Comment/s
            value_to_write = ""
            for y in dictionary_of_comments[i]:
                if value_to_write == "":
                    value_to_write = "%s" % (y)
                else:
                    value_to_write = "%s <br>%s" % (value_to_write, y)
            self.report.write('<td>{0}</td>\n'.format(value_to_write))

            self.report.write('</tr>\n')
        self.report.write('</table>\n')

    def CreateDeviationTable(self):
        self.report.write('<table>\n')
        self.report.write('<tr>\n')
        self.report.write('<th>Incident ID</th>\n')
        self.report.write('<th>Test case</th>\n')
        self.report.write('<th>Requirement</th>\n')
        if self.deviation_assesment_avaliable:
            self.report.write('<th>Blocking</th>\n')
            self.report.write('<th>Comment</th>\n')
        self.report.write('</tr>\n')

        # create a dictionary starting from the data
        dictionary_of_incident = collections.OrderedDict()

        for test_result in self.files:
            self.Config = configparser.RawConfigParser()
            self.Config.read(test_result)

            tc_id = self.Config.get(section="GENERIC", option="test case number")
            requirement = self.Config.get(section="GENERIC", option="requirement cover")
            # result = self.Config.get(section="GENERIC", option="result")
            incident = self.Config.get(section="GENERIC", option="incident number")

            # Fill the dictionary
            if incident != "":
                if incident not in dictionary_of_incident.keys():
                    dictionary_of_incident[str(incident)] = {}
                    dictionary_of_incident[str(incident)]["requirement"] = []
                    dictionary_of_incident[str(incident)]["testcase"] = []
                dictionary_of_incident[str(incident)]["requirement"].append(requirement)
                dictionary_of_incident[str(incident)]["testcase"].append(tc_id)

        # Start to write on the table the data contained in the dictionary
        for i in dictionary_of_incident.keys():
            self.report.write('<tr>\n')

            # Write the incident
            self.report.write('<td nowrap><a href="https://jira.zdv.liebherr.i/browse/{0}" target="_blank">{0}</a></td>\n'.format(i))

            # write the TestCase/s
            value_to_write = ""
            for y in dictionary_of_incident[i]["testcase"]:
                if value_to_write == "":
                    value_to_write = y
                else:
                    value_to_write = value_to_write + "<br>" + y
            self.report.write('<td>{0}</td>\n'.format(value_to_write))

            # write the requirement/s
            value_to_write = ""
            for y in dictionary_of_incident[i]["requirement"]:
                if value_to_write == "":
                    value_to_write = y
                else:
                    value_to_write = value_to_write + "<br>" + y
            self.report.write('<td>{0}</td>\n'.format(value_to_write))

            # Write the assesment
            if self.deviation_assesment_avaliable:
                if self.deviation_assesment[i]["blocking"] == "YES":
                    color = "#FF0000"
                else:
                    color = "#00FF00"
                self.report.write('<td bgcolor="{1}">{0}</td>\n'.format(self.deviation_assesment[i]["blocking"], color))
                self.report.write('<td>{0}</td>\n'.format(self.deviation_assesment[i]["comment"]))

            self.report.write('</tr>\n')

        self.report.write('</table>\n')

    def CreateDetailsTable(self):

        for test_result in self.files:
            self.Config = configparser.RawConfigParser()
            self.Config.read(test_result)

            tc_id = self.Config.get(section="GENERIC", option="test case number")
            requirement = self.Config.get(section="GENERIC", option="requirement cover")
            result = self.Config.get(section="GENERIC", option="result")
            comment = self.Config.get(section="GENERIC", option="comment")
            tester_note = self.Config.get(section="GENERIC", option="tester note")
            execution_date = self.Config.get(section="GENERIC", option="test execution date")
            execution_time = self.Config.get(section="GENERIC", option="test execution time")
            incident = self.Config.get(section="GENERIC", option="incident number")
            try:
                session_id = self.Config.get(section="GENERIC", option="test session id")
            except Exception:
                session_id = "(NA)"
            description = self.Config.get(section="GENERIC", option="test case description")

            pc_name = self.Config.get(section="ENVIRONMENT", option="pc name")
            user_name = self.Config.get(section="ENVIRONMENT", option="user name")
            sw_number = self.Config.get(section="ENVIRONMENT", option="sw number")
            sw_revision = self.Config.get(section="ENVIRONMENT", option="sw revision")
            hil_model = self.Config.get(section="ENVIRONMENT", option="hil model")
            a2l_master = self.Config.get(section="ENVIRONMENT", option="a2l master")
            a2l_slave = self.Config.get(section="ENVIRONMENT", option="a2l slave")
            bootloader = self.Config.get(section="ENVIRONMENT", option="bootloader")
            checksum_calibration_application = self.Config.get(section="ENVIRONMENT", option="checksum calibration and application")
            ecu_id = self.Config.get(section="ENVIRONMENT", option="ecu id")
            ecu_spf = self.Config.get(section="ENVIRONMENT", option="ecu spf_idx")
            ecu_serial_number = self.Config.get(section="ENVIRONMENT", option="ecu serial_number")
            try:
                harness_id = self.Config.get(section="ENVIRONMENT", option="harness id")
            except Exception:
                harness_id = "(NA)"
            try:
                hil_model_revision = self.Config.get(section="ENVIRONMENT", option="hil model revision number")
            except Exception:
                hil_model_revision = "(NA)"
            try:
                tools_folder_revision = self.Config.get(section="ENVIRONMENT", option="tools folder revision number")
            except Exception:
                tools_folder_revision = "(NA)"

            log = self.Config.get(section="ACTUAL RESULTS", option="log")

            self.report.write('<button class="accordion">{0}</button>\n'.format(tc_id))
            self.report.write('<div class="panel">\n')

            self.report.write('<table>\n')
            self.report.write('<tr>\n')
            self.report.write('<th>TestCase ID</th>\n')
            self.report.write('<td>{0}</td>\n'.format(tc_id))
            self.report.write('</tr>\n')
            self.report.write('<tr>\n')
            self.report.write('<th>Requirement</th>\n')
            requirement = requirement.lstrip()
            requirement = requirement.replace("\n", "<br>")
            self.report.write('<td>{0}</td>\n'.format(requirement))
            self.report.write('<tr>\n')
            self.report.write('<th>Description</th>\n')
            self.report.write('<td>{0}</td>\n'.format(description))
            self.report.write('</tr>\n')
            self.report.write('</tr>\n')
            self.report.write('<tr>\n')
            self.report.write('<th>Execution date</th>\n')
            self.report.write('<td>{0}</td>\n'.format(execution_date))
            self.report.write('</tr>\n')
            self.report.write('<tr>\n')
            self.report.write('<th>Execution time</th>\n')
            self.report.write('<td>{0}</td>\n'.format(execution_time))
            self.report.write('</tr>\n')
            self.report.write('<th>Session ID</th>\n')
            self.report.write('<td>{0}</td>\n'.format(session_id))
            self.report.write('</tr>\n')
            self.report.write('<tr>\n')
            self.report.write('<th>Result</th>\n')
            self.report.write('<td>{0}</td>\n'.format(result))
            self.report.write('</tr>\n')
            self.report.write('<tr>\n')
            self.report.write('<th>Comment</th>\n')
            self.report.write('<td>{0}</td>\n'.format(comment))
            self.report.write('</tr>\n')
            self.report.write('<tr>\n')
            self.report.write('<th>Tester note</th>\n')
            self.report.write('<td>{0}</td>\n'.format(tester_note))
            self.report.write('</tr>\n')
            self.report.write('<tr>\n')
            self.report.write('<th>Incident No</th>\n')
            self.report.write('<td>{0}</td>\n'.format(incident))
            self.report.write('</tr>\n')
            self.report.write('<tr>\n')
            self.report.write('<th>PC name</th>\n')
            self.report.write('<td>{0}</td>\n'.format(pc_name))
            self.report.write('</tr>\n')
            self.report.write('<tr>\n')
            self.report.write('<th>User</th>\n')
            self.report.write('<td>{0}</td>\n'.format(user_name))
            self.report.write('</tr>\n')
            self.report.write('<tr>\n')
            self.report.write('<th>SW number</th>\n')
            self.report.write('<td>{0}</td>\n'.format(sw_number))
            self.report.write('</tr>\n')
            self.report.write('<tr>\n')
            self.report.write('<th>SW revision</th>\n')
            self.report.write('<td>{0}</td>\n'.format(sw_revision))
            self.report.write('</tr>\n')
            self.report.write('<tr>\n')
            self.report.write('<th>tools folder revision</th>\n')
            self.report.write('<td>{0}</td>\n'.format(tools_folder_revision))
            self.report.write('</tr>\n')
            self.report.write('<tr>\n')
            self.report.write('<th>HIL model</th>\n')
            self.report.write('<td>{0}</td>\n'.format(hil_model))
            self.report.write('</tr>\n')
            self.report.write('<tr>\n')
            self.report.write('<th>HIL model revision</th>\n')
            self.report.write('<td>{0}</td>\n'.format(hil_model_revision))
            self.report.write('</tr>\n')
            self.report.write('<tr>\n')
            self.report.write('<th>Harness ID</th>\n')
            self.report.write('<td>{0}</td>\n'.format(harness_id))
            self.report.write('</tr>\n')
            self.report.write('<tr>\n')
            self.report.write('<th>a2l master</th>\n')
            self.report.write('<td>{0}</td>\n'.format(a2l_master))
            self.report.write('</tr>\n')
            self.report.write('<tr>\n')
            self.report.write('<th>a2l slave</th>\n')
            self.report.write('<td>{0}</td>\n'.format(a2l_slave))
            self.report.write('</tr>\n')
            self.report.write('<th>Bootloader</th>\n')
            self.report.write('<td>{0}</td>\n'.format(bootloader))
            self.report.write('</tr>\n')
            self.report.write('<tr>\n')
            self.report.write('<th>Checksum calibration + application</th>\n')
            self.report.write('<td>{0}</td>\n'.format(checksum_calibration_application))
            self.report.write('</tr>\n')
            self.report.write('<tr>\n')
            self.report.write('<th>ECU id</th>\n')
            self.report.write('<td>{0}</td>\n'.format(ecu_id))
            self.report.write('</tr>\n')
            self.report.write('<tr>\n')
            self.report.write('<th>ECU spf</th>\n')
            self.report.write('<td>{0}</td>\n'.format(ecu_spf))
            self.report.write('</tr>\n')
            self.report.write('<tr>\n')
            self.report.write('<th>ECU serial number</th>\n')
            self.report.write('<td>{0}</td>\n'.format(ecu_serial_number))
            self.report.write('</tr>\n')

            self.report.write('<tr>\n')
            value_to_write = ""
            log = log.split("\n")
            for line in log:
                if re.search(r'\d\d:\d\d:\d\d', line) is None:
                    value_to_write = value_to_write + "<br>" + "<font color = 'grey'>\t\t\t\t\t" + line + '</font>\n'
                else:
                    value_to_write = value_to_write + "<br>" + line
            self.report.write('<td colspan = "2">{0}</td>\n'.format(value_to_write))
            self.report.write('</tr>\n')

            self.report.write('</table>\n')
            self.report.write('</div>\n')
