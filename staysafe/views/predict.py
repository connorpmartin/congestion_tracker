"""
staysafe prediction page view.

URLs include:
/predict/
"""
import os
import flask
import staysafe
import sys

@staysafe.app.route('/predict.html', methods=['GET', 'POST'])
def show_prediction():
    connection = staysafe.model.get_db()
    if flask.request.method == 'POST':
        if "building_name" in flask.request.form:
            cur_building_info = connection.execute("SELECT id, building_name "
                                                "FROM buildings WHERE building_name=?",
                                                (flask.request.form['building'],))

            id_name = cur_building_info.fetchone()
            #print(id_name, file=sys.stdout)
            #sys.stdout.flush()

            if id_name is None:
                return flask.render_template("error.html")
                
            selected_id = id_name["id"]
            selected_name = id_name["building_name"]

            print("Day " + flask.request.form["day"], file=sys.stdout)
            print("Time " + flask.request.form["time"], file=sys.stdout)
            sys.stdout.flush()

            cur_cong_level = connection.execute("SELECT cong_level "
                                            "FROM congestion WHERE owner_id=? "
                                            "AND day_of_week=? "
                                            "AND time_period=?",
                                            (selected_id,
                                            flask.request.form["day"],
                                            flask.request.form["time"],))

            info = cur_cong_level.fetchone()
            print("result " + str(info), file=sys.stdout)
            sys.stdout.flush()

            selected_cong_level = info["cong_level"]
            selected_day_of_week = flask.request.form["day"]

            #print(id_name, file=sys.stdout)
            #sys.stdout.flush()

            selected_time_period = flask.request.form["time"]

            # print("selected_cong_level:", selected_cong_level)
            context = {"building_name": selected_name,
                    "day_of_week": selected_day_of_week,
                    "time_period": selected_time_period,
                    "cong_level": selected_cong_level}
            print("result " + str(context), file=sys.stdout)
            sys.stdout.flush()

            return flask.render_template("predict.html", **context)

        if "category" in flask.request.form:
            selected_names_cong_levels = []
            cur_category_info = connection.execute("SELECT id, building_name, category "
                                                    "FROM buildings")
            id_name_category = cur_category_info.fetchall()
            for item in id_name_category:
                if flask.request.form["category"] in item["category"]:
                    cur_cong_level = connection.execute("SELECT cong_level "
                                                        "FROM congestion WHERE owner_id=? "
                                                        "AND day_of_week=? "
                                                        "AND time_period=?",
                                                        (item["id"],
                                                        flask.request.form["day_of_week"],
                                                        flask.request.form["time_period"],))
                    selected_cong_level = cur_cong_level.fetchone()["cong_level"]
                    selected_names_cong_levels.append({
                        "building_name": item["building_name"],
                        "cong_level": selected_cong_level
                    })

            context = {"buildings_info": selected_names_cong_levels,
                        "day_of_week": flask.request.form["day_of_week"],
                        "time_period": flask.request.form["time_period"]}
            return flask.render_template("predict.html", **context)