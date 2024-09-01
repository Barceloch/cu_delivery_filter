odoo.define('cu_delivery_filter.delivery_filter', [], function (require) {
    'use strict';

    console.log("(BarSoft) - delivery_filter.js cargado correctamente");

    $(document).ready(async function() {  // Convertir la función a asíncrona

        try {
            const data = await checkLoggedIn();  // Ahora puedes usar await
            const _loggedin = data.logged_in;
            // if (!_loggedin) {
            //     return;
            // }

            // Verifica si hay un municipio seleccionado en la sesión
            let municipalitySelected = sessionStorage.getItem('municipalitySelected');
            let provinceSelected = sessionStorage.getItem('provinceSelected');

            // Si el usuario está logueado, verificar los datos del partner
            if (_loggedin) {
                const partnerData = await getPartnerDeliveryInfo();

                if (partnerData) {
                    const partnerMunicipality = partnerData.partner_city;
                    const partnerProvince = partnerData.partner_state;

                    console.log('Partner ADDRESS:', partnerProvince, ', ', partnerMunicipality)

                    // Comparar los datos del partner con los seleccionados en la sesión
                    if (partnerMunicipality !== municipalitySelected || partnerProvince !== provinceSelected) {
                        $('#deliveryModal').modal('show');
                    }
                }
            }

            // Mostrar el modal si no se ha seleccionado un municipio
            if (!municipalitySelected || !provinceSelected) {
                $('#deliveryModal').modal('show');
            }

            // Actualizar texto de la dirección
            if (municipalitySelected && provinceSelected) {
                $('#deliveryText').text(provinceSelected + '/' + municipalitySelected);
            } else {
                $('#deliveryText').text('Seleccionar dirección');
            }

            // Abre el modal al hacer clic en "Dirección de entrega"
            $('#deliveryAddress').on('click', function(event) {
                event.preventDefault();
                $('#deliveryModal').modal('show');
            });

            // Agregar la verificación de la dirección antes de acceder a la página de detalles del producto
            const productLinks = document.querySelectorAll('.oe_product_image_link, .o_wsale_products_item_title a');

            productLinks.forEach(function(link) {
                link.addEventListener('click', function(event) {
                    if (!municipalitySelected || !provinceSelected) {
                        event.preventDefault();
                        $('#deliveryModal').modal('show');
                        alert('Por favor, seleccione su provincia y municipio.');
                    }
                });
            });

            $('#cancelModalButton').on('click', function() {
                $('#deliveryModal').modal('hide'); // Cierra el modal
            });

            // Manejar el cambio de provincia
            $('#province').change(async function() {
                const provinceId = $(this).val();
                const municipalitySelect = $('#municipality');

                municipalitySelect.empty();
                municipalitySelect.append('<option value="">Seleccione un municipio</option>');

                if (provinceId) {
                    try {
                        const data = await fetchMunicipalities(provinceId);
                        if (Array.isArray(data.result)) {
                            data.result.forEach(function(municipality) {
                                municipalitySelect.append(`<option value="${municipality.id}">${municipality.name}</option>`);
                            });
                        }
                    } catch (error) {
                        console.error("Error al obtener los municipios:", error);
                    }
                }
            });

            // Manejar el cambio en el campo state_id
            $('select[name="state_id"]').on('change', async function () {
                const stateId = $(this).val();
                const citySelect = $('select[name="city"]');

                citySelect.empty();
                citySelect.append('<option value="">Seleccionar Municipio...</option>');

                if (stateId) {
                    try {
                        const data = await fetchMunicipalities(stateId);
                        if (Array.isArray(data.result)) {
                            data.result.forEach(function (municipality) {
                                citySelect.append(`<option value="${municipality.name}">${municipality.name}</option>`);
                            });
                        }
                    } catch (error) {
                        console.error("Error al obtener los municipios:", error);
                    }
                }
            });



            // Manejar el envío del formulario
            $('#deliveryForm').on('submit', async function(event) {
                event.preventDefault();
                const provinceId = $('#province').val();
                const municipalityId = $('#municipality').val();
                const form = this;

                try {
                    const data = await checkCartItemsCount();
                    const cartHasItems = data.items_count;
                    console.log("cartHasItems:", cartHasItems);

                    if (cartHasItems) {
                        if (confirm("Cambiar la dirección afectará el contenido de su carrito. ¿Desea continuar?")) {
                            sessionStorage.setItem('provinceSelected', $('#province option:selected').data('code'));
                            sessionStorage.setItem('municipalitySelected', $('#municipality option:selected').text());
                            
                            // const province = $('#province option:selected').data('code');
                            // const municipality = $('#municipality option:selected').text();

                            // // Actualiza el texto en el header
                            // updateDeliveryText(province, municipality);

                            form.submit();
                        } else {
                            $('#deliveryModal').modal('hide'); // Cierra el modal
                        }
                    } else {
                        sessionStorage.setItem('provinceSelected', $('#province option:selected').data('code'));
                        sessionStorage.setItem('municipalitySelected', $('#municipality option:selected').text());
                        
                        // const province = $('#province option:selected').data('code');
                        // const municipality = $('#municipality option:selected').text();

                        // // Actualiza el texto en el header
                        // updateDeliveryText(province, municipality);

                        form.submit();
                    }
                } catch (error) {
                    console.error('Error al verificar el carrito:', error);
                }
            });

        } catch (error) {
            console.error('Error en el proceso de inicialización:', error);
        }

        // Función para obtener municipios
        async function fetchMunicipalities(provinceId) {
            try {
                ...
                return response;
            } catch (error) {
                console.error("Error en la llamada AJAX para municipios:", error);
                throw error; // Lanzar el error para que pueda ser capturado por el manejador de errores
            }
        }

        // Función para verificar los artículos del carrito
        async function checkCartItemsCount() {
            try {
               ...
                return response;
            } catch (error) {
                console.error('Error al verificar el carrito:', error);
                throw error; // Lanzar el error para que pueda ser capturado por el manejador de errores
            }
        }

        // Función para verificar que el usuario este logeado
        async function checkLoggedIn() {
            try {
                ...
                return response;
            } catch (error) {
                console.error('Error al verificar que el usuario esté logeado:', error);
                throw error; // Lanzar el error para que pueda ser capturado por el manejador de errores
            }
        }

        // Función para obtener la información de entrega del partner
        async function getPartnerDeliveryInfo() {
            try {
               ...
                return response;
            } catch (error) {
                console.error('Error al obtener la información de entrega del partner:', error);
                throw error; // Lanzar el error para que pueda ser capturado por el manejador de errores
            }
        }

    });
});
