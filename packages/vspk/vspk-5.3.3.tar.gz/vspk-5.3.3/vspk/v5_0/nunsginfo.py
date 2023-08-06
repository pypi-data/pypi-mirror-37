# -*- coding: utf-8 -*-
#
# Copyright (c) 2015, Alcatel-Lucent Inc, 2017 Nokia
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the copyright holder nor the names of its contributors
#       may be used to endorse or promote products derived from this software without
#       specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.



from bambou import NURESTObject


class NUNSGInfo(NURESTObject):
    """ Represents a NSGInfo in the VSD

        Notes:
            Device information coming from the NSG
    """

    __rest_name__ = "nsginfo"
    __resource_name__ = "nsginfos"

    
    ## Constants
    
    CONST_FAMILY_NSG_E200 = "NSG_E200"
    
    CONST_FAMILY_NSG_C = "NSG_C"
    
    CONST_FAMILY_ANY = "ANY"
    
    CONST_FAMILY_NSG_E = "NSG_E"
    
    CONST_FAMILY_NSG_AMI = "NSG_AMI"
    
    CONST_FAMILY_NSG_X200 = "NSG_X200"
    
    CONST_ENTITY_SCOPE_GLOBAL = "GLOBAL"
    
    CONST_FAMILY_NSG_V = "NSG_V"
    
    CONST_ENTITY_SCOPE_ENTERPRISE = "ENTERPRISE"
    
    CONST_FAMILY_NSG_E300 = "NSG_E300"
    
    CONST_FAMILY_NSG_AZ = "NSG_AZ"
    
    CONST_FAMILY_NSG_DOCKER = "NSG_DOCKER"
    
    CONST_FAMILY_NSG_X = "NSG_X"
    
    

    def __init__(self, **kwargs):
        """ Initializes a NSGInfo instance

            Notes:
                You can specify all parameters while calling this methods.
                A special argument named `data` will enable you to load the
                object from a Python dictionary

            Examples:
                >>> nsginfo = NUNSGInfo(id=u'xxxx-xxx-xxx-xxx', name=u'NSGInfo')
                >>> nsginfo = NUNSGInfo(data=my_dict)
        """

        super(NUNSGInfo, self).__init__()

        # Read/Write Attributes
        
        self._mac_address = None
        self._aar_application_release_date = None
        self._aar_application_version = None
        self._bios_release_date = None
        self._bios_version = None
        self._sku = None
        self._tpm_status = None
        self._tpm_version = None
        self._cpu_type = None
        self._nsg_version = None
        self._uuid = None
        self._family = None
        self._patches_detail = None
        self._serial_number = None
        self._libraries = None
        self._entity_scope = None
        self._product_name = None
        self._associated_entity_type = None
        self._associated_ns_gateway_id = None
        self._external_id = None
        
        self.expose_attribute(local_name="mac_address", remote_name="MACAddress", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="aar_application_release_date", remote_name="AARApplicationReleaseDate", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="aar_application_version", remote_name="AARApplicationVersion", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="bios_release_date", remote_name="BIOSReleaseDate", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="bios_version", remote_name="BIOSVersion", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="sku", remote_name="SKU", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="tpm_status", remote_name="TPMStatus", attribute_type=int, is_required=False, is_unique=False)
        self.expose_attribute(local_name="tpm_version", remote_name="TPMVersion", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="cpu_type", remote_name="CPUType", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="nsg_version", remote_name="NSGVersion", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="uuid", remote_name="UUID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="family", remote_name="family", attribute_type=str, is_required=False, is_unique=False, choices=[u'ANY', u'NSG_AMI', u'NSG_AZ', u'NSG_C', u'NSG_DOCKER', u'NSG_E', u'NSG_E200', u'NSG_E300', u'NSG_V', u'NSG_X', u'NSG_X200'])
        self.expose_attribute(local_name="patches_detail", remote_name="patchesDetail", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="serial_number", remote_name="serialNumber", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="libraries", remote_name="libraries", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="entity_scope", remote_name="entityScope", attribute_type=str, is_required=False, is_unique=False, choices=[u'ENTERPRISE', u'GLOBAL'])
        self.expose_attribute(local_name="product_name", remote_name="productName", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="associated_entity_type", remote_name="associatedEntityType", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="associated_ns_gateway_id", remote_name="associatedNSGatewayID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="external_id", remote_name="externalID", attribute_type=str, is_required=False, is_unique=True)
        

        self._compute_args(**kwargs)

    # Properties
    
    @property
    def mac_address(self):
        """ Get mac_address value.

            Notes:
                MAC Address of the NSG.  May represent the MAC address of the first uplink that came operational during bootstrapping.

                
                This attribute is named `MACAddress` in VSD API.
                
        """
        return self._mac_address

    @mac_address.setter
    def mac_address(self, value):
        """ Set mac_address value.

            Notes:
                MAC Address of the NSG.  May represent the MAC address of the first uplink that came operational during bootstrapping.

                
                This attribute is named `MACAddress` in VSD API.
                
        """
        self._mac_address = value

    
    @property
    def aar_application_release_date(self):
        """ Get aar_application_release_date value.

            Notes:
                Release Date of the AAR Application

                
                This attribute is named `AARApplicationReleaseDate` in VSD API.
                
        """
        return self._aar_application_release_date

    @aar_application_release_date.setter
    def aar_application_release_date(self, value):
        """ Set aar_application_release_date value.

            Notes:
                Release Date of the AAR Application

                
                This attribute is named `AARApplicationReleaseDate` in VSD API.
                
        """
        self._aar_application_release_date = value

    
    @property
    def aar_application_version(self):
        """ Get aar_application_version value.

            Notes:
                The AAR Application Version

                
                This attribute is named `AARApplicationVersion` in VSD API.
                
        """
        return self._aar_application_version

    @aar_application_version.setter
    def aar_application_version(self, value):
        """ Set aar_application_version value.

            Notes:
                The AAR Application Version

                
                This attribute is named `AARApplicationVersion` in VSD API.
                
        """
        self._aar_application_version = value

    
    @property
    def bios_release_date(self):
        """ Get bios_release_date value.

            Notes:
                Release Date of the NSG BiOS

                
                This attribute is named `BIOSReleaseDate` in VSD API.
                
        """
        return self._bios_release_date

    @bios_release_date.setter
    def bios_release_date(self, value):
        """ Set bios_release_date value.

            Notes:
                Release Date of the NSG BiOS

                
                This attribute is named `BIOSReleaseDate` in VSD API.
                
        """
        self._bios_release_date = value

    
    @property
    def bios_version(self):
        """ Get bios_version value.

            Notes:
                NSG BIOS Version as received from the NSG during bootstrap or a reboot.  If the information exeeds 255 characters, the extra characters will be truncated.

                
                This attribute is named `BIOSVersion` in VSD API.
                
        """
        return self._bios_version

    @bios_version.setter
    def bios_version(self, value):
        """ Set bios_version value.

            Notes:
                NSG BIOS Version as received from the NSG during bootstrap or a reboot.  If the information exeeds 255 characters, the extra characters will be truncated.

                
                This attribute is named `BIOSVersion` in VSD API.
                
        """
        self._bios_version = value

    
    @property
    def sku(self):
        """ Get sku value.

            Notes:
                The part number of the NSG

                
                This attribute is named `SKU` in VSD API.
                
        """
        return self._sku

    @sku.setter
    def sku(self, value):
        """ Set sku value.

            Notes:
                The part number of the NSG

                
                This attribute is named `SKU` in VSD API.
                
        """
        self._sku = value

    
    @property
    def tpm_status(self):
        """ Get tpm_status value.

            Notes:
                TPM status code as reported by the NSG during bootstrapping. This informate indicates if TPM is being used in securing the private key/certificate of an NSG. Possible values are 0(Unknown), 1(Enabled_Not_Operational), 2(Enabled_Operational), 3(Disabled).

                
                This attribute is named `TPMStatus` in VSD API.
                
        """
        return self._tpm_status

    @tpm_status.setter
    def tpm_status(self, value):
        """ Set tpm_status value.

            Notes:
                TPM status code as reported by the NSG during bootstrapping. This informate indicates if TPM is being used in securing the private key/certificate of an NSG. Possible values are 0(Unknown), 1(Enabled_Not_Operational), 2(Enabled_Operational), 3(Disabled).

                
                This attribute is named `TPMStatus` in VSD API.
                
        """
        self._tpm_status = value

    
    @property
    def tpm_version(self):
        """ Get tpm_version value.

            Notes:
                TPM (Trusted Platform Module) version as reported by the NSG.

                
                This attribute is named `TPMVersion` in VSD API.
                
        """
        return self._tpm_version

    @tpm_version.setter
    def tpm_version(self, value):
        """ Set tpm_version value.

            Notes:
                TPM (Trusted Platform Module) version as reported by the NSG.

                
                This attribute is named `TPMVersion` in VSD API.
                
        """
        self._tpm_version = value

    
    @property
    def cpu_type(self):
        """ Get cpu_type value.

            Notes:
                The NSG Processor Type based on information extracted during bootstrapping.  This may refer to a type of processor manufactured by Intel, ARM, AMD, Cyrix, VIA, or others.

                
                This attribute is named `CPUType` in VSD API.
                
        """
        return self._cpu_type

    @cpu_type.setter
    def cpu_type(self, value):
        """ Set cpu_type value.

            Notes:
                The NSG Processor Type based on information extracted during bootstrapping.  This may refer to a type of processor manufactured by Intel, ARM, AMD, Cyrix, VIA, or others.

                
                This attribute is named `CPUType` in VSD API.
                
        """
        self._cpu_type = value

    
    @property
    def nsg_version(self):
        """ Get nsg_version value.

            Notes:
                The NSG Version as reported during a bootstrap or a reboot of the NSG. 

                
                This attribute is named `NSGVersion` in VSD API.
                
        """
        return self._nsg_version

    @nsg_version.setter
    def nsg_version(self, value):
        """ Set nsg_version value.

            Notes:
                The NSG Version as reported during a bootstrap or a reboot of the NSG. 

                
                This attribute is named `NSGVersion` in VSD API.
                
        """
        self._nsg_version = value

    
    @property
    def uuid(self):
        """ Get uuid value.

            Notes:
                The Redhat/CentOS UUID of the NSG

                
                This attribute is named `UUID` in VSD API.
                
        """
        return self._uuid

    @uuid.setter
    def uuid(self, value):
        """ Set uuid value.

            Notes:
                The Redhat/CentOS UUID of the NSG

                
                This attribute is named `UUID` in VSD API.
                
        """
        self._uuid = value

    
    @property
    def family(self):
        """ Get family value.

            Notes:
                The NSG Family type as it was returned by the NSG during bootstrapping.

                
        """
        return self._family

    @family.setter
    def family(self, value):
        """ Set family value.

            Notes:
                The NSG Family type as it was returned by the NSG during bootstrapping.

                
        """
        self._family = value

    
    @property
    def patches_detail(self):
        """ Get patches_detail value.

            Notes:
                Base64 Encoded JSON String of the extra details pertaining to each successfully installed patch

                
                This attribute is named `patchesDetail` in VSD API.
                
        """
        return self._patches_detail

    @patches_detail.setter
    def patches_detail(self, value):
        """ Set patches_detail value.

            Notes:
                Base64 Encoded JSON String of the extra details pertaining to each successfully installed patch

                
                This attribute is named `patchesDetail` in VSD API.
                
        """
        self._patches_detail = value

    
    @property
    def serial_number(self):
        """ Get serial_number value.

            Notes:
                The NSG's serial number as it is stored in the system's CMOS (Motherboard)

                
                This attribute is named `serialNumber` in VSD API.
                
        """
        return self._serial_number

    @serial_number.setter
    def serial_number(self, value):
        """ Set serial_number value.

            Notes:
                The NSG's serial number as it is stored in the system's CMOS (Motherboard)

                
                This attribute is named `serialNumber` in VSD API.
                
        """
        self._serial_number = value

    
    @property
    def libraries(self):
        """ Get libraries value.

            Notes:
                Tracks RPM package installed for some libraries installed on the NSG.

                
        """
        return self._libraries

    @libraries.setter
    def libraries(self, value):
        """ Set libraries value.

            Notes:
                Tracks RPM package installed for some libraries installed on the NSG.

                
        """
        self._libraries = value

    
    @property
    def entity_scope(self):
        """ Get entity_scope value.

            Notes:
                Specify if scope of entity is Data center or Enterprise level

                
                This attribute is named `entityScope` in VSD API.
                
        """
        return self._entity_scope

    @entity_scope.setter
    def entity_scope(self, value):
        """ Set entity_scope value.

            Notes:
                Specify if scope of entity is Data center or Enterprise level

                
                This attribute is named `entityScope` in VSD API.
                
        """
        self._entity_scope = value

    
    @property
    def product_name(self):
        """ Get product_name value.

            Notes:
                NSG Product Name as reported when the device bootstraps.

                
                This attribute is named `productName` in VSD API.
                
        """
        return self._product_name

    @product_name.setter
    def product_name(self, value):
        """ Set product_name value.

            Notes:
                NSG Product Name as reported when the device bootstraps.

                
                This attribute is named `productName` in VSD API.
                
        """
        self._product_name = value

    
    @property
    def associated_entity_type(self):
        """ Get associated_entity_type value.

            Notes:
                Object type of the associated entity.

                
                This attribute is named `associatedEntityType` in VSD API.
                
        """
        return self._associated_entity_type

    @associated_entity_type.setter
    def associated_entity_type(self, value):
        """ Set associated_entity_type value.

            Notes:
                Object type of the associated entity.

                
                This attribute is named `associatedEntityType` in VSD API.
                
        """
        self._associated_entity_type = value

    
    @property
    def associated_ns_gateway_id(self):
        """ Get associated_ns_gateway_id value.

            Notes:
                The ID of the NSG from which the infomation was collected.

                
                This attribute is named `associatedNSGatewayID` in VSD API.
                
        """
        return self._associated_ns_gateway_id

    @associated_ns_gateway_id.setter
    def associated_ns_gateway_id(self, value):
        """ Set associated_ns_gateway_id value.

            Notes:
                The ID of the NSG from which the infomation was collected.

                
                This attribute is named `associatedNSGatewayID` in VSD API.
                
        """
        self._associated_ns_gateway_id = value

    
    @property
    def external_id(self):
        """ Get external_id value.

            Notes:
                External object ID. Used for integration with third party systems

                
                This attribute is named `externalID` in VSD API.
                
        """
        return self._external_id

    @external_id.setter
    def external_id(self, value):
        """ Set external_id value.

            Notes:
                External object ID. Used for integration with third party systems

                
                This attribute is named `externalID` in VSD API.
                
        """
        self._external_id = value

    

    