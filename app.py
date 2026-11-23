import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(page_title="GreenAsset | Sustainability",page_icon="🌱",layout="wide")
st.title("GreenAsset")
st.caption("Building Sustainability Screening | Scenario-based estimates")
st.warning("Screening tool only. Results are indicative and are not an energy audit, GRIHA/IGBC/LEED certification or engineering design.")
st.sidebar.header("Building inputs")
area=st.sidebar.number_input("Built-up area (m²)",100.0,100000.0,5000.0,100.0)
occupants=st.sidebar.number_input("Occupants",1,10000,250,5)
electricity=st.sidebar.number_input("Annual electricity use (kWh/m²)",1.0,500.0,110.0,5.0)
water=st.sidebar.number_input("Daily water demand (litres/person)",10.0,500.0,135.0,5.0)
roof=st.sidebar.number_input("Usable roof area (m²)",0.0,50000.0,900.0,50.0)
rain=st.sidebar.number_input("Annual rainfall (mm)",0.0,5000.0,900.0,50.0)
solar_eff=st.sidebar.slider("PV system capacity factor (%)",5,30,18)
st.subheader("Baseline performance")
annual_kwh=area*electricity
annual_water=occupants*water*365/1000
# Illustrative factors, editable by the user
grid_factor=st.number_input("Grid emission factor (kg CO₂/kWh)",0.1,2.0,0.716,0.001)
carbon=annual_kwh*grid_factor/1000
solar_kw=roof*solar_eff/100
solar_generation=solar_kw*4.5*365
rain_harvest=roof*rain/1000*.8
c1,c2,c3,c4=st.columns(4)
c1.metric("Annual electricity",f"{annual_kwh/1e6:.2f} GWh")
c2.metric("Operational emissions",f"{carbon:,.0f} tCO₂/year")
c3.metric("Annual water demand",f"{annual_water:,.0f} kL")
c4.metric("Rainwater harvest potential",f"{rain_harvest:,.0f} kL/year")
st.subheader("Improvement scenario")
energy_save=st.slider("Energy efficiency improvement (%)",0,50,20)
water_save=st.slider("Water efficiency improvement (%)",0,50,25)
solar_share=st.slider("Solar generation used on-site (%)",0,100,80)
new_energy=annual_kwh*(1-energy_save/100)
solar_used=min(solar_generation*solar_share/100,new_energy)
grid_after=max(0,new_energy-solar_used)
carbon_after=grid_after*grid_factor/1000
water_after=annual_water*(1-water_save/100)
scenario=pd.DataFrame({"Metric":["Electricity demand (MWh)","Grid electricity (MWh)","Operational emissions (tCO₂)","Water demand (kL)"],"Baseline":[annual_kwh/1000,annual_kwh/1000,carbon,annual_water],"Scenario":[new_energy/1000,grid_after/1000,carbon_after,water_after]})
st.plotly_chart(px.bar(scenario.melt("Metric",var_name="Case",value_name="Value"),x="Metric",y="Value",color="Case",barmode="group",title="Baseline vs improvement scenario"),use_container_width=True)
st.subheader("Indicative solar and rainwater opportunities")
x,y=st.columns(2)
with x:
    st.metric("Potential PV capacity",f"{solar_kw:.1f} kWp")
    st.metric("Estimated annual PV generation",f"{solar_generation/1000:.1f} MWh")
with y:
    st.metric("Potential annual rainwater capture",f"{rain_harvest:.1f} kL")
    st.metric("Estimated post-efficiency water demand",f"{water_after:.1f} kL")
st.download_button("Download scenario results",scenario.to_csv(index=False).encode(),"sustainability_scenario.csv","text/csv")
st.info("Assumptions: 4.5 equivalent full-sun hours/day, 80% rainwater collection efficiency and user-entered grid factor. Actual yields depend on location, shading, system design, climate and operating conditions.")
